from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import TOPICS, Config, TaskStatus
from app.core.dto.task import TaskStatusStrDTO
from app.core.interfaces.repositories.analytics_repo import AnalyticsRepositoryInterface


class MongoRepository(AnalyticsRepositoryInterface):
    def __init__(self, config: Config):
        self.config = config
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(config.MONGO_URI)
        self.db: AsyncIOMotorDatabase = self.client.get_database(config.MONGO_DATABASE)

    async def filter(self, collection: TOPICS, **filters) -> list:
        collection = getattr(self.db, collection)
        results = await collection.find(filters).to_list(None)
        return results

    async def get_tasks_statuses(
        self, collection: TOPICS, project_id: int, exclude_task_ids: list[int] = None
    ) -> list[TaskStatusStrDTO]:
        collection = getattr(self.db, collection)
        if exclude_task_ids is None:
            exclude_task_ids = []

        tasks = await collection.aggregate(
            [
                {
                    "$lookup": {
                        "from": TOPICS.TASK_DELETED.value,
                        "localField": "task_id",
                        "foreignField": "task_id",
                        "as": "deleted_task",
                    }
                },
                {
                    "$match": {
                        "deleted_task": [],
                        "project_id": project_id,
                        "task_id": {"$nin": exclude_task_ids},
                    }
                },
                {"$sort": {"created_at": -1}},
                {
                    "$group": {
                        "_id": "$task_id",
                        "task_id": {"$first": "$task_id"},
                        "status": {"$first": "$status"},
                        "created_at": {"$first": "$created_at"},
                    }
                },
                {"$project": {"task_id": 1, "status": 1, "_id": 0}},
            ]
        ).to_list(None)

        return [
            TaskStatusStrDTO(task_id=task["task_id"], status=task["status"])
            for task in tasks
        ]

    async def count_completed_tasks_by_user(
        self, collection: TOPICS, project_id: int, user_id: int
    ) -> int:
        collection = getattr(self.db, collection)
        week_ago = datetime.now() - timedelta(days=7)

        count_result = await collection.aggregate(
            [
                {
                    "$lookup": {
                        "from": TOPICS.TASK_DELETED.value,
                        "localField": "task_id",
                        "foreignField": "task_id",
                        "as": "deleted_task",
                    },
                },
                {
                    "$match": {
                        "project_id": project_id,
                        "user_id": user_id,
                        "status": TaskStatus.DONE.value,
                        "created_at": {"$gt": week_ago},
                        "deleted_task": [],
                    }
                },
                {"$group": {"_id": None, "count": {"$sum": 1}}},
            ]
        ).to_list(None)

        count = count_result[0]["count"] if count_result else 0

        return count

    async def get_avg_time_to_complete(
        self, collection: TOPICS, project_id: int
    ) -> int:
        collection = getattr(self.db, collection)
        avg_time_result = await collection.aggregate(
            [
                {
                    "$lookup": {
                        "from": TOPICS.TASK_DELETED.value,
                        "localField": "task_id",
                        "foreignField": "task_id",
                        "as": "deleted_task",
                    },
                },
                {
                    "$match": {
                        "project_id": project_id,
                        "status": TaskStatus.DONE.value,
                        "deleted_task": [],
                    }
                },
                {
                    "$group": {
                        "_id": "$project_id",
                        "avg_time": {
                            "$avg": {"$subtract": ["$created_at", "$task_started_time"]}
                        },
                    }
                },
            ]
        ).to_list(None)

        avg_time_seconds = int(
            (avg_time_result[0]["avg_time"] if avg_time_result else 0) / 1000
        )
        return avg_time_seconds
