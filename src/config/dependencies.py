from fastapi.security import HTTPBearer
from services.data import DataService
from services.pipeline import PipelineService

security = HTTPBearer()

data_service = DataService(
    base_url="http://localhost:8000",
    data_path="../restaurants_data_manual_recat.json"
)
pipeline = PipelineService(data_service=data_service)