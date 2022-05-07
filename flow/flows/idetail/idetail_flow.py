import os
from typing import List

from prefect import flatten, unmapped

from flows.abstract_flow_on_demand import AbstractFlowOnDemand
from flows.idetail.idetail_settings import IdetailDemands, IdetailTasks

PROJECT_NAME = os.getenv('PREFECT_PROJECT_NAME', 'etude-Prefect')

class IdetailFlow(AbstractFlowOnDemand):
    def __init__(self):
        super().__init__(name="idetail_flow", meta_tasks=IdetailTasks())

    def build(self, demands: List[IdetailDemands] = [IdetailDemands.update_status_by_s3_raw_data_path_task]):
        super().build(demands)

    def build_basic_flow(self):
        self.meta_tasks.get_csv_resource_data_by_product_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "product_name": self.meta_tasks.get_products_task
            },
            flow=self.basic_flow,
        )

        self.meta_tasks.get_csv_master_data_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "resource_data": flatten(self.meta_tasks.get_csv_resource_data_by_product_task),
                "master_csv_path": unmapped(self.meta_tasks.get_paths_of_master_csv_task)
            },
            flow=self.basic_flow,
        )

        self.meta_tasks.delete_contents_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "resource_data": flatten(self.meta_tasks.get_csv_resource_data_by_product_task)
            },
            flow=self.basic_flow
        )

        self.meta_tasks.register_contents_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "master_data": self.meta_tasks.get_csv_master_data_task,
                "resource_data": flatten(self.meta_tasks.get_csv_resource_data_by_product_task)
            },
            upstream_tasks=[
                self.meta_tasks.delete_contents_task,
            ],
            flow=self.basic_flow,
        )

        self.meta_tasks.update_resources_by_product_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "product_name": self.meta_tasks.get_products_task,
                "resource_data": self.meta_tasks.get_csv_resource_data_by_product_task
            },
            flow=self.basic_flow,
        )

        self.meta_tasks.update_status_by_s3_raw_data_path_task.set_dependencies(
            mapped=True,
            keyword_tasks={
                "resource_data": self.meta_tasks.get_csv_resource_data_by_product_task
            },
            upstream_tasks=[
                self.meta_tasks.register_contents_task,
                self.meta_tasks.update_resources_by_product_task
            ],
            flow=self.basic_flow,
        )
