from fastapi.security import HTTPBearer
from services.data import DataService
from services.pipeline import PipelineService

security = HTTPBearer()

data_service = DataService()
pipeline = PipelineService(data_service=data_service)