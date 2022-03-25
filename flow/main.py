import os
from datetime import datetime
from typing import List

import prefect
from prefect import Client, Flow, Task, Parameter
from prefect.executors import LocalDaskExecutor
from prefect.run_configs import UniversalRun
from prefect.storage import Local
from prefect.tasks.notifications.email_task import EmailTask

PROJECT_NAME = os.getenv('PREFECT_PROJECT_NAME', 'etude-Prefect')

class AbstractFlow:
    def __init__(self, flow_name: str = "no_named_flow", parameters: List[Task] = [], e_tasks: List[Task] = [], t_tasks: List[Task] = [], l_tasks: List[Task] = []) -> None:
        self.flow = Flow(
            name=flow_name,
            run_config=UniversalRun(),
            storage=Local(add_default_labels=False),
            executor=LocalDaskExecutor())

        for parameter in parameters:
            self.flow.add_task(parameter)

        self.e_tasks = e_tasks
        self.t_tasks = t_tasks
        self.l_tasks = l_tasks

    def register(self):
        self.extract()
        self.transform()
        self.load()

        return self.flow.register(project_name=PROJECT_NAME)

    def run(self, flow_id: str, parameters: dict = {}):
        Client().create_flow_run(flow_id=flow_id, parameters=parameters)


    def extract(self):
        for e_task in self.e_tasks:
            self.flow.add_task(e_task)

    def transform(self):
        for t_task in self.t_tasks:
            self.flow.add_task(t_task)

    def load(self):
        for l_task in self.l_tasks:
            self.flow.add_task(l_task)

class SayHelloTask(Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.module_name = 'say_hello_task'


    def run(self, from_date: datetime = None, **kwargs):
        flow_params = prefect.context.get("parameters", {})

        self.logger.info(f'Hello World! {flow_params=} {type(from_date)=} {from_date=}')

# Setup prefect cloud client and create project
Client().create_project(project_name=PROJECT_NAME)

# Setup parameters
message_parameter = Parameter('msg', default='this is parameter')
datetime_parameter = prefect.core.parameter.DateTimeParameter('from_date', required=False)

# Setup tasks
email_task = EmailTask(
    subject='Prefect Notification - Flow finished',
    msg='This message is sent with AWS SES SMTP.',
    smtp_server='email-smtp.ap-northeast-1.amazonaws.com',
    email_from='<Email address needs domain that it was verified identities in Amazon SES>',
    email_to='')

# Setup flow
basicFlow = AbstractFlow(
    flow_name="basicFlow",
    parameters=[message_parameter, datetime_parameter],
    e_tasks=[SayHelloTask()],
    t_tasks=[],
    l_tasks=[])

# Register flow
flow_id = basicFlow.register()

# Run flow
basicFlow.run(flow_id=flow_id, parameters={'msg': "Run registered flow.", 'from_date': "2022-02-17T20:13:00+09:00"})
