from dataclasses import dataclass

from prefect import Task

from flows.abstract_settings import AbstractDemands, AbstractTasks
from tasks.idetail.delete_contents_task import DeleteContentsTask
from tasks.idetail.get_csv_master_data_task import GetCsvMasterDataTask
from tasks.idetail.get_csv_resource_data_by_product_task import GetCsvResourceDataByProductTask
from tasks.idetail.get_paths_of_master_csv_task import GetPathsOfMasterCsvTask
from tasks.idetail.get_products_task import GetProductsTask
from tasks.idetail.register_contents_task import RegisterContentsTask
from tasks.idetail.update_resources_by_product_task import UpdateResourcesByProductTask
from tasks.idetail.update_status_by_s3_raw_data_path_task import UpdateStatusByS3RawDataPathTask


@dataclass
class IdetailDemands(AbstractDemands):
    get_products_task: str = "get_products_task"
    get_csv_resource_data_by_product_task: str = "get_csv_resource_data_by_product_task"
    get_paths_of_master_csv_task: str = "get_paths_of_master_csv_task"
    get_csv_master_data_task: str = "get_csv_master_data_task"
    delete_contents_task: str = "delete_contents_task"
    register_contents_task: str = "register_contents_task"
    update_resources_by_product_task: str = "update_resources_by_product_task"
    update_status_by_s3_raw_data_path_task: str = "update_status_by_s3_raw_data_path_task"


@dataclass
class IdetailTasks(AbstractTasks):
    get_products_task: Task = GetProductsTask()
    get_csv_resource_data_by_product_task: Task = GetCsvResourceDataByProductTask()
    get_paths_of_master_csv_task: Task = GetPathsOfMasterCsvTask()
    get_csv_master_data_task: Task = GetCsvMasterDataTask()
    delete_contents_task: Task = DeleteContentsTask()
    register_contents_task: Task = RegisterContentsTask()
    update_resources_by_product_task: Task = UpdateResourcesByProductTask()
    update_status_by_s3_raw_data_path_task: Task = UpdateStatusByS3RawDataPathTask()
