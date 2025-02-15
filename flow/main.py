import os

import prefect
from prefect import Client, Parameter
from prefect.tasks.notifications.email_task import EmailTask

from flows.idetail.idetail_flow import IdetailFlow
from flows.idetail.idetail_settings import IdetailDemands

PROJECT_NAME = os.getenv('PREFECT_PROJECT_NAME', 'etude-Prefect')

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
idetail_flow = IdetailFlow()

# Build flow
idetail_flow.build(demands=[IdetailDemands.get_csv_master_data_task, IdetailDemands.get_csv_resource_data_by_product_task])

# Register flow
idetail_flow_id = idetail_flow.register()

# Run flow
idetail_flow.run(flow_id=idetail_flow_id, parameters={})
