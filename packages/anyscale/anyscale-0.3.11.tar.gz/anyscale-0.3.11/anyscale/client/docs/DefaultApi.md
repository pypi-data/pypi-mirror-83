# openapi_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get**](DefaultApi.md#apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get) | **GET** /api/v2/clouds/gcp/enable/api/{project_id}/{api_name} | Apis Enable
[**change_password_api_v2_users_change_password_post**](DefaultApi.md#change_password_api_v2_users_change_password_post) | **POST** /api/v2/users/change_password | Change Password
[**check_availability_api_v2_organizations_check_availability_get**](DefaultApi.md#check_availability_api_v2_organizations_check_availability_get) | **GET** /api/v2/organizations/check_availability | Check Availability
[**check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get**](DefaultApi.md#check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get) | **GET** /api/v2/userinfo/check_is_feature_flag_on | Check Is Feature Flag On
[**create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get**](DefaultApi.md#create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get) | **GET** /api/v2/clouds/gcp/create/anyscale_service_account/{target_project_id} | Create Anyscale Service Account
[**create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get**](DefaultApi.md#create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get) | **GET** /api/v2/clouds/gcp/create/autoscaler_service_account/{project_id} | Create Autoscaler Service Account
[**create_cloud_api_v2_clouds_post**](DefaultApi.md#create_cloud_api_v2_clouds_post) | **POST** /api/v2/clouds/ | Create Cloud
[**create_from_github_api_v2_projects_create_from_github_post**](DefaultApi.md#create_from_github_api_v2_projects_create_from_github_post) | **POST** /api/v2/projects/create_from_github | Create From Github
[**create_invitation_api_v2_organization_invitations_post**](DefaultApi.md#create_invitation_api_v2_organization_invitations_post) | **POST** /api/v2/organization_invitations/ | Create Invitation
[**create_new_session_api_v2_sessions_create_from_snapshot_post**](DefaultApi.md#create_new_session_api_v2_sessions_create_from_snapshot_post) | **POST** /api/v2/sessions/create_from_snapshot | Create New Session
[**create_new_session_api_v2_sessions_create_new_session_post**](DefaultApi.md#create_new_session_api_v2_sessions_create_new_session_post) | **POST** /api/v2/sessions/create_new_session | Create New Session
[**create_project_api_v2_projects_post**](DefaultApi.md#create_project_api_v2_projects_post) | **POST** /api/v2/projects/ | Create Project
[**create_project_collaborator_api_v2_projects_project_id_collaborators_post**](DefaultApi.md#create_project_collaborator_api_v2_projects_project_id_collaborators_post) | **POST** /api/v2/projects/{project_id}/collaborators | Create Project Collaborator
[**create_snapshot_api_v2_snapshots_post**](DefaultApi.md#create_snapshot_api_v2_snapshots_post) | **POST** /api/v2/snapshots/ | Create Snapshot
[**delete_cloud_api_v2_clouds_cloud_id_delete**](DefaultApi.md#delete_cloud_api_v2_clouds_cloud_id_delete) | **DELETE** /api/v2/clouds/{cloud_id} | Delete Cloud
[**delete_project_api_v2_projects_project_id_delete**](DefaultApi.md#delete_project_api_v2_projects_project_id_delete) | **DELETE** /api/v2/projects/{project_id} | Delete Project
[**delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete**](DefaultApi.md#delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete) | **DELETE** /api/v2/projects/{project_id}/collaborators/{role_or_identity_id} | Delete Project Collaborator
[**delete_session_api_v2_sessions_session_id_delete**](DefaultApi.md#delete_session_api_v2_sessions_session_id_delete) | **DELETE** /api/v2/sessions/{session_id} | Delete Session
[**delete_snapshot_api_v2_snapshots_snapshot_id_delete**](DefaultApi.md#delete_snapshot_api_v2_snapshots_snapshot_id_delete) | **DELETE** /api/v2/snapshots/{snapshot_id} | Delete Snapshot
[**deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete**](DefaultApi.md#deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete) | **DELETE** /api/v2/autosync_sessions/{autosync_session_id} | Deregister Autosync Session
[**describe_session_api_v2_sessions_session_id_describe_get**](DefaultApi.md#describe_session_api_v2_sessions_session_id_describe_get) | **GET** /api/v2/sessions/{session_id}/describe | Describe Session
[**execute_command_api_v2_sessions_session_id_execute_command_name_post**](DefaultApi.md#execute_command_api_v2_sessions_session_id_execute_command_name_post) | **POST** /api/v2/sessions/{session_id}/execute/{command_name} | Execute Command
[**execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post**](DefaultApi.md#execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post) | **POST** /api/v2/sessions/{session_id}/execute_interactive_command | Execute Interactive Command
[**execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post**](DefaultApi.md#execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post) | **POST** /api/v2/sessions/{session_id}/execute_shell_command | Execute Shell Command
[**find_cloud_by_name_api_v2_clouds_find_by_name_post**](DefaultApi.md#find_cloud_by_name_api_v2_clouds_find_by_name_post) | **POST** /api/v2/clouds/find_by_name | Find Cloud By Name
[**find_project_by_project_name_api_v2_projects_find_by_name_get**](DefaultApi.md#find_project_by_project_name_api_v2_projects_find_by_name_get) | **GET** /api/v2/projects/find_by_name | Find Project By Project Name
[**find_with_invitation_api_v2_organizations_find_with_invitation_get**](DefaultApi.md#find_with_invitation_api_v2_organizations_find_with_invitation_get) | **GET** /api/v2/organizations/find_with_invitation | Find With Invitation
[**find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get**](DefaultApi.md#find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get) | **GET** /api/v2/organizations/find_with_public_identifier | Find With Public Identifier
[**finish_session_command_api_v2_session_commands_session_command_id_finish_post**](DefaultApi.md#finish_session_command_api_v2_session_commands_session_command_id_finish_post) | **POST** /api/v2/session_commands/{session_command_id}/finish | Finish Session Command
[**fork_session_api_v2_sessions_session_id_fork_post**](DefaultApi.md#fork_session_api_v2_sessions_session_id_fork_post) | **POST** /api/v2/sessions/{session_id}/fork | Fork Session
[**gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get**](DefaultApi.md#gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get) | **GET** /api/v2/clouds/gcp/create/{cloud_name} | Gcp Create Cloud
[**gcp_create_project_api_v2_clouds_gcp_create_project_get**](DefaultApi.md#gcp_create_project_api_v2_clouds_gcp_create_project_get) | **GET** /api/v2/clouds/gcp/create/project | Gcp Create Project
[**get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get**](DefaultApi.md#get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get) | **GET** /api/v2/autosync_sessions/ | Get Active Autosync Sessions For Session
[**get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get**](DefaultApi.md#get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get) | **GET** /api/v2/clouds/anyscale/aws_account | Get Anyscale Aws Account
[**get_anyscale_version_api_v2_userinfo_anyscale_version_get**](DefaultApi.md#get_anyscale_version_api_v2_userinfo_anyscale_version_get) | **GET** /api/v2/userinfo/anyscale_version | Get Anyscale Version
[**get_cloud_api_v2_clouds_cloud_id_get**](DefaultApi.md#get_cloud_api_v2_clouds_cloud_id_get) | **GET** /api/v2/clouds/{cloud_id} | Get Cloud
[**get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get**](DefaultApi.md#get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get) | **GET** /api/v2/session_commands/{session_command_id}/execution_logs | Get Execution Logs
[**get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get**](DefaultApi.md#get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get) | **GET** /api/v2/session_commands/{session_command_id}/execution_logs_archived | Get Execution Logs Archived
[**get_invitation_api_v2_organization_invitations_invitation_id_get**](DefaultApi.md#get_invitation_api_v2_organization_invitations_invitation_id_get) | **GET** /api/v2/organization_invitations/{invitation_id} | Get Invitation
[**get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get**](DefaultApi.md#get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get) | **GET** /api/v2/sessions/{session_id}/monitor_logs | Get Monitor Logs
[**get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get**](DefaultApi.md#get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get) | **GET** /api/v2/sessions/{session_id}/monitor_logs_archived | Get Monitor Logs Archived
[**get_project_api_v2_projects_project_id_get**](DefaultApi.md#get_project_api_v2_projects_project_id_get) | **GET** /api/v2/projects/{project_id} | Get Project
[**get_project_default_session_name_api_v2_projects_project_id_default_session_name_get**](DefaultApi.md#get_project_default_session_name_api_v2_projects_project_id_default_session_name_get) | **GET** /api/v2/projects/{project_id}/default_session_name | Get Project Default Session Name
[**get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get**](DefaultApi.md#get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get) | **GET** /api/v2/projects/{project_id}/latest_cluster_config | Get Project Latest Cluster Config
[**get_session_api_v2_sessions_session_id_get**](DefaultApi.md#get_session_api_v2_sessions_session_id_get) | **GET** /api/v2/sessions/{session_id} | Get Session
[**get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get**](DefaultApi.md#get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get) | **GET** /api/v2/sessions/{session_id}/autoscaler_credentials | Get Session Autoscaler Credentials
[**get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get**](DefaultApi.md#get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get) | **GET** /api/v2/sessions/{session_id}/cluster_config | Get Session Cluster Config
[**get_session_commands_history_api_v2_session_commands_get**](DefaultApi.md#get_session_commands_history_api_v2_session_commands_get) | **GET** /api/v2/session_commands/ | Get Session Commands History
[**get_session_details_api_v2_sessions_session_id_details_get**](DefaultApi.md#get_session_details_api_v2_sessions_session_id_details_get) | **GET** /api/v2/sessions/{session_id}/details | Get Session Details
[**get_session_head_ip_api_v2_sessions_session_id_head_ip_get**](DefaultApi.md#get_session_head_ip_api_v2_sessions_session_id_head_ip_get) | **GET** /api/v2/sessions/{session_id}/head_ip | Get Session Head Ip
[**get_session_history_api_v2_sessions_session_id_history_get**](DefaultApi.md#get_session_history_api_v2_sessions_session_id_history_get) | **GET** /api/v2/sessions/{session_id}/history | Get Session History
[**get_session_overview_api_v2_overview_get**](DefaultApi.md#get_session_overview_api_v2_overview_get) | **GET** /api/v2/overview | Get Session Overview
[**get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get**](DefaultApi.md#get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get) | **GET** /api/v2/sessions/{session_id}/ssh_key | Get Session Ssh Key
[**get_snapshot_api_v2_snapshots_snapshot_id_get**](DefaultApi.md#get_snapshot_api_v2_snapshots_snapshot_id_get) | **GET** /api/v2/snapshots/{snapshot_id} | Get Snapshot
[**get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get**](DefaultApi.md#get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get) | **GET** /api/v2/snapshots/{snapshot_id}/cluster_config | Get Snapshot Cluster Config
[**get_snapshot_files_api_v2_snapshots_snapshot_id_files_get**](DefaultApi.md#get_snapshot_files_api_v2_snapshots_snapshot_id_files_get) | **GET** /api/v2/snapshots/{snapshot_id}/files | Get Snapshot Files
[**get_startup_logs_api_v2_sessions_session_id_startup_logs_get**](DefaultApi.md#get_startup_logs_api_v2_sessions_session_id_startup_logs_get) | **GET** /api/v2/sessions/{session_id}/startup_logs | Get Startup Logs
[**get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get**](DefaultApi.md#get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get) | **GET** /api/v2/sessions/{session_id}/startup_logs_archived | Get Startup Logs Archived
[**get_user_info_api_v2_userinfo_get**](DefaultApi.md#get_user_info_api_v2_userinfo_get) | **GET** /api/v2/userinfo/ | Get User Info
[**google_auth_api_v2_oauth2_google_auth_cloud_name_get**](DefaultApi.md#google_auth_api_v2_oauth2_google_auth_cloud_name_get) | **GET** /api/v2/oauth2/google/auth/{cloud_name} | Google Auth
[**google_callback_api_v2_oauth2_google_callback_get**](DefaultApi.md#google_callback_api_v2_oauth2_google_callback_get) | **GET** /api/v2/oauth2/google/callback | Google Callback
[**handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post**](DefaultApi.md#handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post) | **POST** /api/v2/cloudgateway/{gateway_id} | Handle Gateway Interaction
[**heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post**](DefaultApi.md#heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post) | **POST** /api/v2/autosync_sessions/{autosync_session_id}/heartbeat | Heartbeat
[**iam_create_api_v2_clouds_gcp_create_iam_project_id_get**](DefaultApi.md#iam_create_api_v2_clouds_gcp_create_iam_project_id_get) | **GET** /api/v2/clouds/gcp/create/iam/{project_id} | Iam Create
[**invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post**](DefaultApi.md#invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post) | **POST** /api/v2/organization_invitations/{invitation_id}/invalidate | Invalidate Invitation
[**kill_session_command_api_v2_session_commands_session_command_id_kill_post**](DefaultApi.md#kill_session_command_api_v2_session_commands_session_command_id_kill_post) | **POST** /api/v2/session_commands/{session_command_id}/kill | Kill Session Command
[**list_clouds_api_v2_clouds_get**](DefaultApi.md#list_clouds_api_v2_clouds_get) | **GET** /api/v2/clouds/ | List Clouds
[**list_project_collaborators_api_v2_projects_project_id_collaborators_get**](DefaultApi.md#list_project_collaborators_api_v2_projects_project_id_collaborators_get) | **GET** /api/v2/projects/{project_id}/collaborators | List Project Collaborators
[**list_projects_api_v2_projects_get**](DefaultApi.md#list_projects_api_v2_projects_get) | **GET** /api/v2/projects/ | List Projects
[**list_sessions_api_v2_sessions_get**](DefaultApi.md#list_sessions_api_v2_sessions_get) | **GET** /api/v2/sessions/ | List Sessions
[**list_snapshots_api_v2_snapshots_get**](DefaultApi.md#list_snapshots_api_v2_snapshots_get) | **GET** /api/v2/snapshots/ | List Snapshots
[**login_user_api_v2_users_login_post**](DefaultApi.md#login_user_api_v2_users_login_post) | **POST** /api/v2/users/login | Login User
[**logout_user_api_v2_users_logout_post**](DefaultApi.md#logout_user_api_v2_users_logout_post) | **POST** /api/v2/users/logout | Logout User
[**patch_project_api_v2_projects_project_id_patch**](DefaultApi.md#patch_project_api_v2_projects_project_id_patch) | **PATCH** /api/v2/projects/{project_id} | Patch Project
[**patch_session_api_v2_sessions_session_id_patch**](DefaultApi.md#patch_session_api_v2_sessions_session_id_patch) | **PATCH** /api/v2/sessions/{session_id} | Patch Session
[**patch_snapshot_api_v2_snapshots_snapshot_id_patch**](DefaultApi.md#patch_snapshot_api_v2_snapshots_snapshot_id_patch) | **PATCH** /api/v2/snapshots/{snapshot_id} | Patch Snapshot
[**put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put**](DefaultApi.md#put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put) | **PUT** /api/v2/sessions/{session_id}/cluster_config | Put Session Cluster Config
[**put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put**](DefaultApi.md#put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put) | **PUT** /api/v2/snapshots/{snapshot_id}/cluster_config | Put Snapshot Cluster Config
[**register_autosync_session_api_v2_autosync_sessions_post**](DefaultApi.md#register_autosync_session_api_v2_autosync_sessions_post) | **POST** /api/v2/autosync_sessions/ | Register Autosync Session
[**register_user_api_v2_users_post**](DefaultApi.md#register_user_api_v2_users_post) | **POST** /api/v2/users/ | Register User
[**request_password_reset_api_v2_users_request_password_reset_post**](DefaultApi.md#request_password_reset_api_v2_users_request_password_reset_post) | **POST** /api/v2/users/request_password_reset | Request Password Reset
[**rerun_command_api_v2_session_commands_session_command_id_rerun_post**](DefaultApi.md#rerun_command_api_v2_session_commands_session_command_id_rerun_post) | **POST** /api/v2/session_commands/{session_command_id}/rerun | Rerun Command
[**reset_password_api_v2_users_reset_password_post**](DefaultApi.md#reset_password_api_v2_users_reset_password_post) | **POST** /api/v2/users/reset_password | Reset Password
[**session_finish_up_api_v2_sessions_session_id_finish_up_post**](DefaultApi.md#session_finish_up_api_v2_sessions_session_id_finish_up_post) | **POST** /api/v2/sessions/{session_id}/finish_up | Session Finish Up
[**session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get**](DefaultApi.md#session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get) | **GET** /api/v2/sessions/{session_id}/anyscale_wheel | Session Get Anyscale Wheel
[**session_report_command_api_v2_session_commands_session_command_id_report_command_post**](DefaultApi.md#session_report_command_api_v2_session_commands_session_command_id_report_command_post) | **POST** /api/v2/session_commands/{session_command_id}/report_command | Session Report Command
[**session_up_api_v2_sessions_up_post**](DefaultApi.md#session_up_api_v2_sessions_up_post) | **POST** /api/v2/sessions/up | Session Up
[**set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post**](DefaultApi.md#set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post) | **POST** /api/v2/sessions/{session_id}/ray_dashboard_url | Set Ray Dashboard Url
[**setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get**](DefaultApi.md#setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get) | **GET** /api/v2/clouds/gcp/setup_billing/{project_id} | Setup Billing
[**start_session_api_v2_sessions_session_id_start_post**](DefaultApi.md#start_session_api_v2_sessions_session_id_start_post) | **POST** /api/v2/sessions/{session_id}/start | Start Session
[**stop_session_api_v2_sessions_session_id_stop_post**](DefaultApi.md#stop_session_api_v2_sessions_session_id_stop_post) | **POST** /api/v2/sessions/{session_id}/stop | Stop Session
[**take_snapshot_api_v2_sessions_session_id_take_snapshot_post**](DefaultApi.md#take_snapshot_api_v2_sessions_session_id_take_snapshot_post) | **POST** /api/v2/sessions/{session_id}/take_snapshot | Take Snapshot
[**upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post**](DefaultApi.md#upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post) | **POST** /api/v2/session_commands/{session_command_id}/upload_logs | Upload Session Command Logs
[**user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get**](DefaultApi.md#user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get) | **GET** /api/v2/users/temporary_aws_credentials | User Get Temporary Aws Credentials
[**user_resend_email_api_v2_users_resend_email_post**](DefaultApi.md#user_resend_email_api_v2_users_resend_email_post) | **POST** /api/v2/users/resend_email | User Resend Email
[**user_server_session_token_api_v2_users_server_session_token_post**](DefaultApi.md#user_server_session_token_api_v2_users_server_session_token_post) | **POST** /api/v2/users/server_session_token | User Server Session Token
[**user_verify_api_v2_users_verify_token_get**](DefaultApi.md#user_verify_api_v2_users_verify_token_get) | **GET** /api/v2/users/verify/{token} | User Verify
[**validate_cluster_api_v2_sessions_validate_cluster_post**](DefaultApi.md#validate_cluster_api_v2_sessions_validate_cluster_post) | **POST** /api/v2/sessions/validate_cluster | Validate Cluster
[**verify_reset_password_token_api_v2_users_reset_password_token_get**](DefaultApi.md#verify_reset_password_token_api_v2_users_reset_password_token_get) | **GET** /api/v2/users/reset_password/{token} | Verify Reset Password Token


# **apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get**
> object apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get(project_id, api_name, block=block)

Apis Enable

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
api_name = 'api_name_example' # str | 
block = True # bool |  (optional) (default to True)

    try:
        # Apis Enable
        api_response = api_instance.apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get(project_id, api_name, block=block)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->apis_enable_api_v2_clouds_gcp_enable_api_project_id_api_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **api_name** | **str**|  | 
 **block** | **bool**|  | [optional] [default to True]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **change_password_api_v2_users_change_password_post**
> change_password_api_v2_users_change_password_post(change_password_params)

Change Password

Changes user's password if they provide their current password.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    change_password_params = openapi_client.ChangePasswordParams() # ChangePasswordParams | 

    try:
        # Change Password
        api_instance.change_password_api_v2_users_change_password_post(change_password_params)
    except ApiException as e:
        print("Exception when calling DefaultApi->change_password_api_v2_users_change_password_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **change_password_params** | [**ChangePasswordParams**](ChangePasswordParams.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_availability_api_v2_organizations_check_availability_get**
> OrganizationavailabilityResponse check_availability_api_v2_organizations_check_availability_get(organization_name)

Check Availability

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    organization_name = 'organization_name_example' # str | 

    try:
        # Check Availability
        api_response = api_instance.check_availability_api_v2_organizations_check_availability_get(organization_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->check_availability_api_v2_organizations_check_availability_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_name** | **str**|  | 

### Return type

[**OrganizationavailabilityResponse**](OrganizationavailabilityResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get**
> FeatureflagresponseResponse check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(flag_key)

Check Is Feature Flag On

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    flag_key = 'flag_key_example' # str | 

    try:
        # Check Is Feature Flag On
        api_response = api_instance.check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get(flag_key)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->check_is_feature_flag_on_api_v2_userinfo_check_is_feature_flag_on_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **flag_key** | **str**|  | 

### Return type

[**FeatureflagresponseResponse**](FeatureflagresponseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get**
> object create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get(target_project_id)

Create Anyscale Service Account

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    target_project_id = 'target_project_id_example' # str | 

    try:
        # Create Anyscale Service Account
        api_response = api_instance.create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get(target_project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_anyscale_service_account_api_v2_clouds_gcp_create_anyscale_service_account_target_project_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **target_project_id** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get**
> object create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get(project_id)

Create Autoscaler Service Account

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Create Autoscaler Service Account
        api_response = api_instance.create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_autoscaler_service_account_api_v2_clouds_gcp_create_autoscaler_service_account_project_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_cloud_api_v2_clouds_post**
> CloudResponse create_cloud_api_v2_clouds_post(write_cloud)

Create Cloud

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    write_cloud = openapi_client.WriteCloud() # WriteCloud | 

    try:
        # Create Cloud
        api_response = api_instance.create_cloud_api_v2_clouds_post(write_cloud)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_cloud_api_v2_clouds_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **write_cloud** | [**WriteCloud**](WriteCloud.md)|  | 

### Return type

[**CloudResponse**](CloudResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**409** |  names have to be unique.  |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_from_github_api_v2_projects_create_from_github_post**
> GithubprojectResponse create_from_github_api_v2_projects_create_from_github_post(create_from_github_options)

Create From Github

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_from_github_options = openapi_client.CreateFromGithubOptions() # CreateFromGithubOptions | 

    try:
        # Create From Github
        api_response = api_instance.create_from_github_api_v2_projects_create_from_github_post(create_from_github_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_from_github_api_v2_projects_create_from_github_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_from_github_options** | [**CreateFromGithubOptions**](CreateFromGithubOptions.md)|  | 

### Return type

[**GithubprojectResponse**](GithubprojectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_invitation_api_v2_organization_invitations_post**
> OrganizationinvitationbaseResponse create_invitation_api_v2_organization_invitations_post(create_organization_invitation)

Create Invitation

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_organization_invitation = openapi_client.CreateOrganizationInvitation() # CreateOrganizationInvitation | 

    try:
        # Create Invitation
        api_response = api_instance.create_invitation_api_v2_organization_invitations_post(create_organization_invitation)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_invitation_api_v2_organization_invitations_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_organization_invitation** | [**CreateOrganizationInvitation**](CreateOrganizationInvitation.md)|  | 

### Return type

[**OrganizationinvitationbaseResponse**](OrganizationinvitationbaseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_session_api_v2_sessions_create_from_snapshot_post**
> SessionidResponse create_new_session_api_v2_sessions_create_from_snapshot_post(create_session_from_snapshot_options)

Create New Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_session_from_snapshot_options = openapi_client.CreateSessionFromSnapshotOptions() # CreateSessionFromSnapshotOptions | 

    try:
        # Create New Session
        api_response = api_instance.create_new_session_api_v2_sessions_create_from_snapshot_post(create_session_from_snapshot_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_new_session_api_v2_sessions_create_from_snapshot_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_session_from_snapshot_options** | [**CreateSessionFromSnapshotOptions**](CreateSessionFromSnapshotOptions.md)|  | 

### Return type

[**SessionidResponse**](SessionidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_new_session_api_v2_sessions_create_new_session_post**
> SessionidResponse create_new_session_api_v2_sessions_create_new_session_post(create_session_from_snapshot_options)

Create New Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_session_from_snapshot_options = openapi_client.CreateSessionFromSnapshotOptions() # CreateSessionFromSnapshotOptions | 

    try:
        # Create New Session
        api_response = api_instance.create_new_session_api_v2_sessions_create_new_session_post(create_session_from_snapshot_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_new_session_api_v2_sessions_create_new_session_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_session_from_snapshot_options** | [**CreateSessionFromSnapshotOptions**](CreateSessionFromSnapshotOptions.md)|  | 

### Return type

[**SessionidResponse**](SessionidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_project_api_v2_projects_post**
> ProjectbaseResponse create_project_api_v2_projects_post(write_project)

Create Project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    write_project = openapi_client.WriteProject() # WriteProject | 

    try:
        # Create Project
        api_response = api_instance.create_project_api_v2_projects_post(write_project)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_project_api_v2_projects_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **write_project** | [**WriteProject**](WriteProject.md)|  | 

### Return type

[**ProjectbaseResponse**](ProjectbaseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**409** | Project names have to be unique. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_project_collaborator_api_v2_projects_project_id_collaborators_post**
> create_project_collaborator_api_v2_projects_project_id_collaborators_post(project_id, write_project_collaborator)

Create Project Collaborator

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
write_project_collaborator = openapi_client.WriteProjectCollaborator() # WriteProjectCollaborator | 

    try:
        # Create Project Collaborator
        api_instance.create_project_collaborator_api_v2_projects_project_id_collaborators_post(project_id, write_project_collaborator)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_project_collaborator_api_v2_projects_project_id_collaborators_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **write_project_collaborator** | [**WriteProjectCollaborator**](WriteProjectCollaborator.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**409** | User must be the owner of the project to add collaborators. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_snapshot_api_v2_snapshots_post**
> SnapshotcreateResponse create_snapshot_api_v2_snapshots_post(create_snapshot_options)

Create Snapshot

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_snapshot_options = openapi_client.CreateSnapshotOptions() # CreateSnapshotOptions | 

    try:
        # Create Snapshot
        api_response = api_instance.create_snapshot_api_v2_snapshots_post(create_snapshot_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->create_snapshot_api_v2_snapshots_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_snapshot_options** | [**CreateSnapshotOptions**](CreateSnapshotOptions.md)|  | 

### Return type

[**SnapshotcreateResponse**](SnapshotcreateResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cloud_api_v2_clouds_cloud_id_delete**
> delete_cloud_api_v2_clouds_cloud_id_delete(cloud_id)

Delete Cloud

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_id = 'cloud_id_example' # str | 

    try:
        # Delete Cloud
        api_instance.delete_cloud_api_v2_clouds_cloud_id_delete(cloud_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_cloud_api_v2_clouds_cloud_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project_api_v2_projects_project_id_delete**
> delete_project_api_v2_projects_project_id_delete(project_id)

Delete Project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Delete Project
        api_instance.delete_project_api_v2_projects_project_id_delete(project_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_project_api_v2_projects_project_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**409** | The state of the project is not deletable. This is most likely due to there being unterminated sessions in this project. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete**
> delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete(project_id, role_or_identity_id)

Delete Project Collaborator

Delete a collaborator from a project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
role_or_identity_id = 'role_or_identity_id_example' # str | 

    try:
        # Delete Project Collaborator
        api_instance.delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete(project_id, role_or_identity_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_project_collaborator_api_v2_projects_project_id_collaborators_role_or_identity_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **role_or_identity_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**409** | User must be the owner of the project to remove collaborators. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_session_api_v2_sessions_session_id_delete**
> delete_session_api_v2_sessions_session_id_delete(session_id)

Delete Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Delete Session
        api_instance.delete_session_api_v2_sessions_session_id_delete(session_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_session_api_v2_sessions_session_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**409** | The state of the session is not deletable. This is most likely due to it being non-terminated. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_snapshot_api_v2_snapshots_snapshot_id_delete**
> SnapshotdeleteResponse delete_snapshot_api_v2_snapshots_snapshot_id_delete(snapshot_id)

Delete Snapshot

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 

    try:
        # Delete Snapshot
        api_response = api_instance.delete_snapshot_api_v2_snapshots_snapshot_id_delete(snapshot_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->delete_snapshot_api_v2_snapshots_snapshot_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 

### Return type

[**SnapshotdeleteResponse**](SnapshotdeleteResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete**
> deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete(autosync_session_id)

Deregister Autosync Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    autosync_session_id = 'autosync_session_id_example' # str | 

    try:
        # Deregister Autosync Session
        api_instance.deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete(autosync_session_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->deregister_autosync_session_api_v2_autosync_sessions_autosync_session_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **autosync_session_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **describe_session_api_v2_sessions_session_id_describe_get**
> SessiondescribeResponse describe_session_api_v2_sessions_session_id_describe_get(session_id)

Describe Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Describe Session
        api_response = api_instance.describe_session_api_v2_sessions_session_id_describe_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->describe_session_api_v2_sessions_session_id_describe_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**SessiondescribeResponse**](SessiondescribeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_command_api_v2_sessions_session_id_execute_command_name_post**
> execute_command_api_v2_sessions_session_id_execute_command_name_post(session_id, command_name, execute_command_options)

Execute Command

Execute a named command on a session.     

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
command_name = 'command_name_example' # str | 
execute_command_options = openapi_client.ExecuteCommandOptions() # ExecuteCommandOptions | 

    try:
        # Execute Command
        api_instance.execute_command_api_v2_sessions_session_id_execute_command_name_post(session_id, command_name, execute_command_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->execute_command_api_v2_sessions_session_id_execute_command_name_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **command_name** | **str**|  | 
 **execute_command_options** | [**ExecuteCommandOptions**](ExecuteCommandOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post**
> ExecutecommandresponseResponse execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post(session_id, execute_shell_command_options)

Execute Interactive Command

Execute an interative command on a session.  This endpoint differs with other execute_* since it doesn't actually execute the command. It will just create the command and return auxiliary information for user to ssh into the head node and run their command.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
execute_shell_command_options = openapi_client.ExecuteShellCommandOptions() # ExecuteShellCommandOptions | 

    try:
        # Execute Interactive Command
        api_response = api_instance.execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post(session_id, execute_shell_command_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **execute_shell_command_options** | [**ExecuteShellCommandOptions**](ExecuteShellCommandOptions.md)|  | 

### Return type

[**ExecutecommandresponseResponse**](ExecutecommandresponseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post**
> SessioncommandidResponse execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post(session_id, execute_shell_command_options)

Execute Shell Command

Execute a shell command on a session.     

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
execute_shell_command_options = openapi_client.ExecuteShellCommandOptions() # ExecuteShellCommandOptions | 

    try:
        # Execute Shell Command
        api_response = api_instance.execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post(session_id, execute_shell_command_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->execute_shell_command_api_v2_sessions_session_id_execute_shell_command_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **execute_shell_command_options** | [**ExecuteShellCommandOptions**](ExecuteShellCommandOptions.md)|  | 

### Return type

[**SessioncommandidResponse**](SessioncommandidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_cloud_by_name_api_v2_clouds_find_by_name_post**
> CloudResponse find_cloud_by_name_api_v2_clouds_find_by_name_post(cloud_name_options)

Find Cloud By Name

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_name_options = openapi_client.CloudNameOptions() # CloudNameOptions | 

    try:
        # Find Cloud By Name
        api_response = api_instance.find_cloud_by_name_api_v2_clouds_find_by_name_post(cloud_name_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->find_cloud_by_name_api_v2_clouds_find_by_name_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_name_options** | [**CloudNameOptions**](CloudNameOptions.md)|  | 

### Return type

[**CloudResponse**](CloudResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**409** | Multiple clouds with the same name. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_project_by_project_name_api_v2_projects_find_by_name_get**
> ProjectListResponse find_project_by_project_name_api_v2_projects_find_by_name_get(name, paging_token=paging_token, count=count)

Find Project By Project Name

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    name = 'name_example' # str | 
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # Find Project By Project Name
        api_response = api_instance.find_project_by_project_name_api_v2_projects_find_by_name_get(name, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->find_project_by_project_name_api_v2_projects_find_by_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**ProjectListResponse**](ProjectListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_with_invitation_api_v2_organizations_find_with_invitation_get**
> OrganizationResponse find_with_invitation_api_v2_organizations_find_with_invitation_get(invitation_id)

Find With Invitation

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    invitation_id = 'invitation_id_example' # str | 

    try:
        # Find With Invitation
        api_response = api_instance.find_with_invitation_api_v2_organizations_find_with_invitation_get(invitation_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->find_with_invitation_api_v2_organizations_find_with_invitation_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **invitation_id** | **str**|  | 

### Return type

[**OrganizationResponse**](OrganizationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Invitation is invalid or inactive. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get**
> OrganizationResponse find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get(public_identifier)

Find With Public Identifier

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    public_identifier = 'public_identifier_example' # str | 

    try:
        # Find With Public Identifier
        api_response = api_instance.find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get(public_identifier)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->find_with_public_identifier_api_v2_organizations_find_with_public_identifier_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **public_identifier** | **str**|  | 

### Return type

[**OrganizationResponse**](OrganizationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | No Organization found with public identifier |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finish_session_command_api_v2_session_commands_session_command_id_finish_post**
> finish_session_command_api_v2_session_commands_session_command_id_finish_post(session_command_id, session_command_finish_options)

Finish Session Command

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 
session_command_finish_options = openapi_client.SessionCommandFinishOptions() # SessionCommandFinishOptions | 

    try:
        # Finish Session Command
        api_instance.finish_session_command_api_v2_session_commands_session_command_id_finish_post(session_command_id, session_command_finish_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->finish_session_command_api_v2_session_commands_session_command_id_finish_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 
 **session_command_finish_options** | [**SessionCommandFinishOptions**](SessionCommandFinishOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fork_session_api_v2_sessions_session_id_fork_post**
> SnapshotidResponse fork_session_api_v2_sessions_session_id_fork_post(session_id, create_session_from_snapshot_options)

Fork Session

Create a copy of a remote session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
create_session_from_snapshot_options = openapi_client.CreateSessionFromSnapshotOptions() # CreateSessionFromSnapshotOptions | 

    try:
        # Fork Session
        api_response = api_instance.fork_session_api_v2_sessions_session_id_fork_post(session_id, create_session_from_snapshot_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->fork_session_api_v2_sessions_session_id_fork_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **create_session_from_snapshot_options** | [**CreateSessionFromSnapshotOptions**](CreateSessionFromSnapshotOptions.md)|  | 

### Return type

[**SnapshotidResponse**](SnapshotidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get**
> object gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get(cloud_name, region)

Gcp Create Cloud

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_name = 'cloud_name_example' # str | 
region = 'region_example' # str | 

    try:
        # Gcp Create Cloud
        api_response = api_instance.gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get(cloud_name, region)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->gcp_create_cloud_api_v2_clouds_gcp_create_cloud_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_name** | **str**|  | 
 **region** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **gcp_create_project_api_v2_clouds_gcp_create_project_get**
> object gcp_create_project_api_v2_clouds_gcp_create_project_get(cloud_name)

Gcp Create Project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_name = 'cloud_name_example' # str | 

    try:
        # Gcp Create Project
        api_response = api_instance.gcp_create_project_api_v2_clouds_gcp_create_project_get(cloud_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->gcp_create_project_api_v2_clouds_gcp_create_project_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_name** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get**
> AutosyncsessionidListResponse get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get(session_id, paging_token=paging_token, count=count)

Get Active Autosync Sessions For Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # Get Active Autosync Sessions For Session
        api_response = api_instance.get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get(session_id, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_active_autosync_sessions_for_session_api_v2_autosync_sessions_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**AutosyncsessionidListResponse**](AutosyncsessionidListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get**
> AnyscaleawsaccountResponse get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()

Get Anyscale Aws Account

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # Get Anyscale Aws Account
        api_response = api_instance.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AnyscaleawsaccountResponse**](AnyscaleawsaccountResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_anyscale_version_api_v2_userinfo_anyscale_version_get**
> AnyscaleversionresponseResponse get_anyscale_version_api_v2_userinfo_anyscale_version_get()

Get Anyscale Version

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # Get Anyscale Version
        api_response = api_instance.get_anyscale_version_api_v2_userinfo_anyscale_version_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_anyscale_version_api_v2_userinfo_anyscale_version_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AnyscaleversionresponseResponse**](AnyscaleversionresponseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cloud_api_v2_clouds_cloud_id_get**
> CloudResponse get_cloud_api_v2_clouds_cloud_id_get(cloud_id)

Get Cloud

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_id = 'cloud_id_example' # str | 

    try:
        # Get Cloud
        api_response = api_instance.get_cloud_api_v2_clouds_cloud_id_get(cloud_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_cloud_api_v2_clouds_cloud_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_id** | **str**|  | 

### Return type

[**CloudResponse**](CloudResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**409** | Multiple clouds with the same ID. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get**
> LogsoutputResponse get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get(session_command_id, log_type, start_line, end_line)

Get Execution Logs

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 
log_type = 'log_type_example' # str | 
start_line = 56 # int | 
end_line = 56 # int | 

    try:
        # Get Execution Logs
        api_response = api_instance.get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get(session_command_id, log_type, start_line, end_line)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_execution_logs_api_v2_session_commands_session_command_id_execution_logs_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 
 **log_type** | **str**|  | 
 **start_line** | **int**|  | 
 **end_line** | **int**|  | 

### Return type

[**LogsoutputResponse**](LogsoutputResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get**
> ArchivedlogsinfoResponse get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get(session_command_id, log_type)

Get Execution Logs Archived

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 
log_type = 'log_type_example' # str | 

    try:
        # Get Execution Logs Archived
        api_response = api_instance.get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get(session_command_id, log_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_execution_logs_archived_api_v2_session_commands_session_command_id_execution_logs_archived_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 
 **log_type** | **str**|  | 

### Return type

[**ArchivedlogsinfoResponse**](ArchivedlogsinfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invitation_api_v2_organization_invitations_invitation_id_get**
> OrganizationinvitationResponse get_invitation_api_v2_organization_invitations_invitation_id_get(invitation_id)

Get Invitation

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    invitation_id = 'invitation_id_example' # str | 

    try:
        # Get Invitation
        api_response = api_instance.get_invitation_api_v2_organization_invitations_invitation_id_get(invitation_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_invitation_api_v2_organization_invitations_invitation_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **invitation_id** | **str**|  | 

### Return type

[**OrganizationinvitationResponse**](OrganizationinvitationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get**
> LogsoutputResponse get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get(session_id, log_type, start_line, end_line)

Get Monitor Logs

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
log_type = 'log_type_example' # str | 
start_line = 56 # int | 
end_line = 56 # int | 

    try:
        # Get Monitor Logs
        api_response = api_instance.get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get(session_id, log_type, start_line, end_line)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_monitor_logs_api_v2_sessions_session_id_monitor_logs_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **log_type** | **str**|  | 
 **start_line** | **int**|  | 
 **end_line** | **int**|  | 

### Return type

[**LogsoutputResponse**](LogsoutputResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get**
> ArchivedlogsinfoResponse get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get(session_id, log_type)

Get Monitor Logs Archived

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
log_type = 'log_type_example' # str | 

    try:
        # Get Monitor Logs Archived
        api_response = api_instance.get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get(session_id, log_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_monitor_logs_archived_api_v2_sessions_session_id_monitor_logs_archived_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **log_type** | **str**|  | 

### Return type

[**ArchivedlogsinfoResponse**](ArchivedlogsinfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project_api_v2_projects_project_id_get**
> ProjectResponse get_project_api_v2_projects_project_id_get(project_id)

Get Project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Get Project
        api_response = api_instance.get_project_api_v2_projects_project_id_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_project_api_v2_projects_project_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project_default_session_name_api_v2_projects_project_id_default_session_name_get**
> ProjectdefaultsessionnameResponse get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(project_id)

Get Project Default Session Name

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Get Project Default Session Name
        api_response = api_instance.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_project_default_session_name_api_v2_projects_project_id_default_session_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**ProjectdefaultsessionnameResponse**](ProjectdefaultsessionnameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get**
> ClusterconfigResponse get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get(project_id)

Get Project Latest Cluster Config

Fetches the latest cluster config of a project. It first checks the latest snapshot and uses that cluster config. If there are no snapshots, it uses the cluster_config saved at the project level.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Get Project Latest Cluster Config
        api_response = api_instance.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**ClusterconfigResponse**](ClusterconfigResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_api_v2_sessions_session_id_get**
> SessionResponse get_session_api_v2_sessions_session_id_get(session_id)

Get Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session
        api_response = api_instance.get_session_api_v2_sessions_session_id_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_api_v2_sessions_session_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**SessionResponse**](SessionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get**
> AutoscalercredentialsResponse get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get(session_id)

Get Session Autoscaler Credentials

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session Autoscaler Credentials
        api_response = api_instance.get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_autoscaler_credentials_api_v2_sessions_session_id_autoscaler_credentials_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**AutoscalercredentialsResponse**](AutoscalercredentialsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get**
> ClusterconfigResponse get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(session_id)

Get Session Cluster Config

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session Cluster Config
        api_response = api_instance.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**ClusterconfigResponse**](ClusterconfigResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_commands_history_api_v2_session_commands_get**
> SessioncommandListResponse get_session_commands_history_api_v2_session_commands_get(session_id, paging_token=paging_token, count=count)

Get Session Commands History

List all commands that have been run on a session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # Get Session Commands History
        api_response = api_instance.get_session_commands_history_api_v2_session_commands_get(session_id, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_commands_history_api_v2_session_commands_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**SessioncommandListResponse**](SessioncommandListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_details_api_v2_sessions_session_id_details_get**
> SessiondetailsResponse get_session_details_api_v2_sessions_session_id_details_get(session_id)

Get Session Details

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session Details
        api_response = api_instance.get_session_details_api_v2_sessions_session_id_details_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_details_api_v2_sessions_session_id_details_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**SessiondetailsResponse**](SessiondetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_head_ip_api_v2_sessions_session_id_head_ip_get**
> HeadipResponse get_session_head_ip_api_v2_sessions_session_id_head_ip_get(session_id)

Get Session Head Ip

Fetches the ip of the head node of the session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session Head Ip
        api_response = api_instance.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_head_ip_api_v2_sessions_session_id_head_ip_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**HeadipResponse**](HeadipResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_history_api_v2_sessions_session_id_history_get**
> SessionhistoryitemListResponse get_session_history_api_v2_sessions_session_id_history_get(session_id, paging_token=paging_token, count=count)

Get Session History

Describe all actions applied to a particular session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # Get Session History
        api_response = api_instance.get_session_history_api_v2_sessions_session_id_history_get(session_id, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_history_api_v2_sessions_session_id_history_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**SessionhistoryitemListResponse**](SessionhistoryitemListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_overview_api_v2_overview_get**
> SessionoverviewListResponse get_session_overview_api_v2_overview_get(paging_token=paging_token, count=count)

Get Session Overview

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # Get Session Overview
        api_response = api_instance.get_session_overview_api_v2_overview_get(paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_overview_api_v2_overview_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**SessionoverviewListResponse**](SessionoverviewListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get**
> SessionsshkeyResponse get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get(session_id)

Get Session Ssh Key

Download SSH needed to log into a given session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Get Session Ssh Key
        api_response = api_instance.get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_session_ssh_key_api_v2_sessions_session_id_ssh_key_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**SessionsshkeyResponse**](SessionsshkeyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_snapshot_api_v2_snapshots_snapshot_id_get**
> SnapshotResponse get_snapshot_api_v2_snapshots_snapshot_id_get(snapshot_id)

Get Snapshot

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 

    try:
        # Get Snapshot
        api_response = api_instance.get_snapshot_api_v2_snapshots_snapshot_id_get(snapshot_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_snapshot_api_v2_snapshots_snapshot_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 

### Return type

[**SnapshotResponse**](SnapshotResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get**
> ClusterconfigResponse get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get(snapshot_id)

Get Snapshot Cluster Config

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 

    try:
        # Get Snapshot Cluster Config
        api_response = api_instance.get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get(snapshot_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 

### Return type

[**ClusterconfigResponse**](ClusterconfigResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_snapshot_files_api_v2_snapshots_snapshot_id_files_get**
> SnapshotfilesResponse get_snapshot_files_api_v2_snapshots_snapshot_id_files_get(snapshot_id)

Get Snapshot Files

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 

    try:
        # Get Snapshot Files
        api_response = api_instance.get_snapshot_files_api_v2_snapshots_snapshot_id_files_get(snapshot_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_snapshot_files_api_v2_snapshots_snapshot_id_files_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 

### Return type

[**SnapshotfilesResponse**](SnapshotfilesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_startup_logs_api_v2_sessions_session_id_startup_logs_get**
> LogsoutputResponse get_startup_logs_api_v2_sessions_session_id_startup_logs_get(session_id, log_type, start_line, end_line)

Get Startup Logs

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
log_type = 'log_type_example' # str | 
start_line = 56 # int | 
end_line = 56 # int | 

    try:
        # Get Startup Logs
        api_response = api_instance.get_startup_logs_api_v2_sessions_session_id_startup_logs_get(session_id, log_type, start_line, end_line)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_startup_logs_api_v2_sessions_session_id_startup_logs_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **log_type** | **str**|  | 
 **start_line** | **int**|  | 
 **end_line** | **int**|  | 

### Return type

[**LogsoutputResponse**](LogsoutputResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get**
> ArchivedlogsinfoResponse get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get(session_id, log_type)

Get Startup Logs Archived

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
log_type = 'log_type_example' # str | 

    try:
        # Get Startup Logs Archived
        api_response = api_instance.get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get(session_id, log_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_startup_logs_archived_api_v2_sessions_session_id_startup_logs_archived_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **log_type** | **str**|  | 

### Return type

[**ArchivedlogsinfoResponse**](ArchivedlogsinfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_info_api_v2_userinfo_get**
> UserinfoResponse get_user_info_api_v2_userinfo_get()

Get User Info

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # Get User Info
        api_response = api_instance.get_user_info_api_v2_userinfo_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->get_user_info_api_v2_userinfo_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**UserinfoResponse**](UserinfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **google_auth_api_v2_oauth2_google_auth_cloud_name_get**
> object google_auth_api_v2_oauth2_google_auth_cloud_name_get(cloud_name)

Google Auth

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    cloud_name = 'cloud_name_example' # str | 

    try:
        # Google Auth
        api_response = api_instance.google_auth_api_v2_oauth2_google_auth_cloud_name_get(cloud_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->google_auth_api_v2_oauth2_google_auth_cloud_name_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_name** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **google_callback_api_v2_oauth2_google_callback_get**
> object google_callback_api_v2_oauth2_google_callback_get()

Google Callback

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # Google Callback
        api_response = api_instance.google_callback_api_v2_oauth2_google_callback_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->google_callback_api_v2_oauth2_google_callback_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post**
> GatewayrequestResponse handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post(gateway_id, json_dumped_gateway_response_message)

Handle Gateway Interaction

Handles requests to and responses from the cloud gateway.  Args:     gateway_message.contents (str): a json dumped gateway dict response message that stores     request ID and data.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    gateway_id = 'gateway_id_example' # str | 
json_dumped_gateway_response_message = openapi_client.JsonDumpedGatewayResponseMessage() # JsonDumpedGatewayResponseMessage | 

    try:
        # Handle Gateway Interaction
        api_response = api_instance.handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post(gateway_id, json_dumped_gateway_response_message)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->handle_gateway_interaction_api_v2_cloudgateway_gateway_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gateway_id** | **str**|  | 
 **json_dumped_gateway_response_message** | [**JsonDumpedGatewayResponseMessage**](JsonDumpedGatewayResponseMessage.md)|  | 

### Return type

[**GatewayrequestResponse**](GatewayrequestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post**
> heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post(autosync_session_id)

Heartbeat

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    autosync_session_id = 'autosync_session_id_example' # str | 

    try:
        # Heartbeat
        api_instance.heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post(autosync_session_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->heartbeat_api_v2_autosync_sessions_autosync_session_id_heartbeat_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **autosync_session_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **iam_create_api_v2_clouds_gcp_create_iam_project_id_get**
> object iam_create_api_v2_clouds_gcp_create_iam_project_id_get(project_id, service_account_email, anyscale_account_email)

Iam Create

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
service_account_email = 'service_account_email_example' # str | 
anyscale_account_email = 'anyscale_account_email_example' # str | 

    try:
        # Iam Create
        api_response = api_instance.iam_create_api_v2_clouds_gcp_create_iam_project_id_get(project_id, service_account_email, anyscale_account_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->iam_create_api_v2_clouds_gcp_create_iam_project_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **service_account_email** | **str**|  | 
 **anyscale_account_email** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post**
> OrganizationinvitationResponse invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post(invitation_id)

Invalidate Invitation

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    invitation_id = 'invitation_id_example' # str | 

    try:
        # Invalidate Invitation
        api_response = api_instance.invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post(invitation_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->invalidate_invitation_api_v2_organization_invitations_invitation_id_invalidate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **invitation_id** | **str**|  | 

### Return type

[**OrganizationinvitationResponse**](OrganizationinvitationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **kill_session_command_api_v2_session_commands_session_command_id_kill_post**
> kill_session_command_api_v2_session_commands_session_command_id_kill_post(session_command_id)

Kill Session Command

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 

    try:
        # Kill Session Command
        api_instance.kill_session_command_api_v2_session_commands_session_command_id_kill_post(session_command_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->kill_session_command_api_v2_session_commands_session_command_id_kill_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_clouds_api_v2_clouds_get**
> CloudListResponse list_clouds_api_v2_clouds_get(paging_token=paging_token, count=count)

List Clouds

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # List Clouds
        api_response = api_instance.list_clouds_api_v2_clouds_get(paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_clouds_api_v2_clouds_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**CloudListResponse**](CloudListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_project_collaborators_api_v2_projects_project_id_collaborators_get**
> ProjectcollaboratorListResponse list_project_collaborators_api_v2_projects_project_id_collaborators_get(project_id, paging_token=paging_token, count=count)

List Project Collaborators

Get a list of all collaborators for a given project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # List Project Collaborators
        api_response = api_instance.list_project_collaborators_api_v2_projects_project_id_collaborators_get(project_id, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_project_collaborators_api_v2_projects_project_id_collaborators_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**ProjectcollaboratorListResponse**](ProjectcollaboratorListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_projects_api_v2_projects_get**
> ProjectListResponse list_projects_api_v2_projects_get(paging_token=paging_token, count=count)

List Projects

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # List Projects
        api_response = api_instance.list_projects_api_v2_projects_get(paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_projects_api_v2_projects_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**ProjectListResponse**](ProjectListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sessions_api_v2_sessions_get**
> SessionListResponse list_sessions_api_v2_sessions_get(project_id, name=name, name_match=name_match, active_only=active_only, paging_token=paging_token, count=count)

List Sessions

List all sessions for a project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
name = 'name_example' # str |  (optional)
name_match = 'name_match_example' # str | a wildcard match for session names. This endpoint will raise an error if both name and name_match is provided. (optional)
active_only = False # bool |  (optional) (default to False)
paging_token = 'paging_token_example' # str |  (optional)
count = 56 # int |  (optional)

    try:
        # List Sessions
        api_response = api_instance.list_sessions_api_v2_sessions_get(project_id, name=name, name_match=name_match, active_only=active_only, paging_token=paging_token, count=count)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_sessions_api_v2_sessions_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **name** | **str**|  | [optional] 
 **name_match** | **str**| a wildcard match for session names. This endpoint will raise an error if both name and name_match is provided. | [optional] 
 **active_only** | **bool**|  | [optional] [default to False]
 **paging_token** | **str**|  | [optional] 
 **count** | **int**|  | [optional] 

### Return type

[**SessionListResponse**](SessionListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_snapshots_api_v2_snapshots_get**
> SnapshotlistResponse list_snapshots_api_v2_snapshots_get(project_id)

List Snapshots

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # List Snapshots
        api_response = api_instance.list_snapshots_api_v2_snapshots_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->list_snapshots_api_v2_snapshots_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

[**SnapshotlistResponse**](SnapshotlistResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_user_api_v2_users_login_post**
> login_user_api_v2_users_login_post(login_user_params)

Login User

Log a user in.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    login_user_params = openapi_client.LoginUserParams() # LoginUserParams | 

    try:
        # Login User
        api_instance.login_user_api_v2_users_login_post(login_user_params)
    except ApiException as e:
        print("Exception when calling DefaultApi->login_user_api_v2_users_login_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_user_params** | [**LoginUserParams**](LoginUserParams.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout_user_api_v2_users_logout_post**
> logout_user_api_v2_users_logout_post()

Logout User

Log a user out.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # Logout User
        api_instance.logout_user_api_v2_users_logout_post()
    except ApiException as e:
        print("Exception when calling DefaultApi->logout_user_api_v2_users_logout_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_project_api_v2_projects_project_id_patch**
> patch_project_api_v2_projects_project_id_patch(project_id, json_patch_operation)

Patch Project

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 
json_patch_operation = [openapi_client.JsonPatchOperation()] # list[JsonPatchOperation] | 

    try:
        # Patch Project
        api_instance.patch_project_api_v2_projects_project_id_patch(project_id, json_patch_operation)
    except ApiException as e:
        print("Exception when calling DefaultApi->patch_project_api_v2_projects_project_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **json_patch_operation** | [**list[JsonPatchOperation]**](JsonPatchOperation.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_session_api_v2_sessions_session_id_patch**
> patch_session_api_v2_sessions_session_id_patch(session_id, json_patch_operation)

Patch Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
json_patch_operation = [openapi_client.JsonPatchOperation()] # list[JsonPatchOperation] | 

    try:
        # Patch Session
        api_instance.patch_session_api_v2_sessions_session_id_patch(session_id, json_patch_operation)
    except ApiException as e:
        print("Exception when calling DefaultApi->patch_session_api_v2_sessions_session_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **json_patch_operation** | [**list[JsonPatchOperation]**](JsonPatchOperation.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**207** | Multi-Status |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_snapshot_api_v2_snapshots_snapshot_id_patch**
> patch_snapshot_api_v2_snapshots_snapshot_id_patch(snapshot_id, json_patch_operation)

Patch Snapshot

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 
json_patch_operation = [openapi_client.JsonPatchOperation()] # list[JsonPatchOperation] | 

    try:
        # Patch Snapshot
        api_instance.patch_snapshot_api_v2_snapshots_snapshot_id_patch(snapshot_id, json_patch_operation)
    except ApiException as e:
        print("Exception when calling DefaultApi->patch_snapshot_api_v2_snapshots_snapshot_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 
 **json_patch_operation** | [**list[JsonPatchOperation]**](JsonPatchOperation.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**207** | Multi-Status |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put**
> put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put(session_id, write_cluster_config)

Put Session Cluster Config

Updates the cluster config of a running session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
write_cluster_config = openapi_client.WriteClusterConfig() # WriteClusterConfig | 

    try:
        # Put Session Cluster Config
        api_instance.put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put(session_id, write_cluster_config)
    except ApiException as e:
        print("Exception when calling DefaultApi->put_session_cluster_config_api_v2_sessions_session_id_cluster_config_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **write_cluster_config** | [**WriteClusterConfig**](WriteClusterConfig.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put**
> put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put(snapshot_id, write_cluster_config)

Put Snapshot Cluster Config

Updates the cluster config of an existing snapshot.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    snapshot_id = 'snapshot_id_example' # str | 
write_cluster_config = openapi_client.WriteClusterConfig() # WriteClusterConfig | 

    try:
        # Put Snapshot Cluster Config
        api_instance.put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put(snapshot_id, write_cluster_config)
    except ApiException as e:
        print("Exception when calling DefaultApi->put_snapshot_cluster_config_api_v2_snapshots_snapshot_id_cluster_config_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **snapshot_id** | **str**|  | 
 **write_cluster_config** | [**WriteClusterConfig**](WriteClusterConfig.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_autosync_session_api_v2_autosync_sessions_post**
> AutosyncsessionidResponse register_autosync_session_api_v2_autosync_sessions_post(session_id)

Register Autosync Session

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Register Autosync Session
        api_response = api_instance.register_autosync_session_api_v2_autosync_sessions_post(session_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->register_autosync_session_api_v2_autosync_sessions_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

[**AutosyncsessionidResponse**](AutosyncsessionidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_user_api_v2_users_post**
> register_user_api_v2_users_post(create_user)

Register User

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    create_user = openapi_client.CreateUser() # CreateUser | 

    try:
        # Register User
        api_instance.register_user_api_v2_users_post(create_user)
    except ApiException as e:
        print("Exception when calling DefaultApi->register_user_api_v2_users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_user** | [**CreateUser**](CreateUser.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**409** | User emails and usernames have to be unique. |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_password_reset_api_v2_users_request_password_reset_post**
> request_password_reset_api_v2_users_request_password_reset_post(request_password_reset_params)

Request Password Reset

Send the user an email with a reset link for a forgotten password.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    request_password_reset_params = openapi_client.RequestPasswordResetParams() # RequestPasswordResetParams | 

    try:
        # Request Password Reset
        api_instance.request_password_reset_api_v2_users_request_password_reset_post(request_password_reset_params)
    except ApiException as e:
        print("Exception when calling DefaultApi->request_password_reset_api_v2_users_request_password_reset_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_password_reset_params** | [**RequestPasswordResetParams**](RequestPasswordResetParams.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rerun_command_api_v2_session_commands_session_command_id_rerun_post**
> rerun_command_api_v2_session_commands_session_command_id_rerun_post(session_command_id)

Rerun Command

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 

    try:
        # Rerun Command
        api_instance.rerun_command_api_v2_session_commands_session_command_id_rerun_post(session_command_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->rerun_command_api_v2_session_commands_session_command_id_rerun_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_password_api_v2_users_reset_password_post**
> reset_password_api_v2_users_reset_password_post(reset_password_params)

Reset Password

Change the user's password to the new password

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    reset_password_params = openapi_client.ResetPasswordParams() # ResetPasswordParams | 

    try:
        # Reset Password
        api_instance.reset_password_api_v2_users_reset_password_post(reset_password_params)
    except ApiException as e:
        print("Exception when calling DefaultApi->reset_password_api_v2_users_reset_password_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reset_password_params** | [**ResetPasswordParams**](ResetPasswordParams.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_finish_up_api_v2_sessions_session_id_finish_up_post**
> session_finish_up_api_v2_sessions_session_id_finish_up_post(session_id, session_finish_up_options)

Session Finish Up

Finishes the session startup assuming the cluster has already been created.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
session_finish_up_options = openapi_client.SessionFinishUpOptions() # SessionFinishUpOptions | 

    try:
        # Session Finish Up
        api_instance.session_finish_up_api_v2_sessions_session_id_finish_up_post(session_id, session_finish_up_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->session_finish_up_api_v2_sessions_session_id_finish_up_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **session_finish_up_options** | [**SessionFinishUpOptions**](SessionFinishUpOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get**
> session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get(session_id)

Session Get Anyscale Wheel

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Session Get Anyscale Wheel
        api_instance.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get(session_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_report_command_api_v2_session_commands_session_command_id_report_command_post**
> session_report_command_api_v2_session_commands_session_command_id_report_command_post(session_command_id, session_report_command_options)

Session Report Command

Reports message for given command.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 
session_report_command_options = openapi_client.SessionReportCommandOptions() # SessionReportCommandOptions | 

    try:
        # Session Report Command
        api_instance.session_report_command_api_v2_session_commands_session_command_id_report_command_post(session_command_id, session_report_command_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->session_report_command_api_v2_session_commands_session_command_id_report_command_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 
 **session_report_command_options** | [**SessionReportCommandOptions**](SessionReportCommandOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **session_up_api_v2_sessions_up_post**
> SessionupresponseResponse session_up_api_v2_sessions_up_post(session_up_options)

Session Up

Creates a placeholder session, but doesn't start the cluster.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_up_options = openapi_client.SessionUpOptions() # SessionUpOptions | 

    try:
        # Session Up
        api_response = api_instance.session_up_api_v2_sessions_up_post(session_up_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->session_up_api_v2_sessions_up_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_up_options** | [**SessionUpOptions**](SessionUpOptions.md)|  | 

### Return type

[**SessionupresponseResponse**](SessionupresponseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post**
> set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post(session_id)

Set Ray Dashboard Url

Fetches the ip of the head node of the session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 

    try:
        # Set Ray Dashboard Url
        api_instance.set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post(session_id)
    except ApiException as e:
        print("Exception when calling DefaultApi->set_ray_dashboard_url_api_v2_sessions_session_id_ray_dashboard_url_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get**
> object setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get(project_id)

Setup Billing

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    project_id = 'project_id_example' # str | 

    try:
        # Setup Billing
        api_response = api_instance.setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get(project_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->setup_billing_api_v2_clouds_gcp_setup_billing_project_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_session_api_v2_sessions_session_id_start_post**
> start_session_api_v2_sessions_session_id_start_post(session_id, start_session_options)

Start Session

Start a (previously stopped) session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
start_session_options = openapi_client.StartSessionOptions() # StartSessionOptions | 

    try:
        # Start Session
        api_instance.start_session_api_v2_sessions_session_id_start_post(session_id, start_session_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->start_session_api_v2_sessions_session_id_start_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **start_session_options** | [**StartSessionOptions**](StartSessionOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_session_api_v2_sessions_session_id_stop_post**
> stop_session_api_v2_sessions_session_id_stop_post(session_id, stop_session_options)

Stop Session

Stop an active session of a project.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
stop_session_options = openapi_client.StopSessionOptions() # StopSessionOptions | 

    try:
        # Stop Session
        api_instance.stop_session_api_v2_sessions_session_id_stop_post(session_id, stop_session_options)
    except ApiException as e:
        print("Exception when calling DefaultApi->stop_session_api_v2_sessions_session_id_stop_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **stop_session_options** | [**StopSessionOptions**](StopSessionOptions.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **take_snapshot_api_v2_sessions_session_id_take_snapshot_post**
> SnapshotidResponse take_snapshot_api_v2_sessions_session_id_take_snapshot_post(session_id, take_snapshot_options)

Take Snapshot

Take a snapshot of a remote session.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_id = 'session_id_example' # str | 
take_snapshot_options = openapi_client.TakeSnapshotOptions() # TakeSnapshotOptions | 

    try:
        # Take Snapshot
        api_response = api_instance.take_snapshot_api_v2_sessions_session_id_take_snapshot_post(session_id, take_snapshot_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->take_snapshot_api_v2_sessions_session_id_take_snapshot_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**|  | 
 **take_snapshot_options** | [**TakeSnapshotOptions**](TakeSnapshotOptions.md)|  | 

### Return type

[**SnapshotidResponse**](SnapshotidResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post**
> UploadsessioncommandlogslocationsResponse upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post(session_command_id)

Upload Session Command Logs

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    session_command_id = 'session_command_id_example' # str | 

    try:
        # Upload Session Command Logs
        api_response = api_instance.upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post(session_command_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->upload_session_command_logs_api_v2_session_commands_session_command_id_upload_logs_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_command_id** | **str**|  | 

### Return type

[**UploadsessioncommandlogslocationsResponse**](UploadsessioncommandlogslocationsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get**
> AwscredentialsResponse user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get()

User Get Temporary Aws Credentials

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # User Get Temporary Aws Credentials
        api_response = api_instance.user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->user_get_temporary_aws_credentials_api_v2_users_temporary_aws_credentials_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**AwscredentialsResponse**](AwscredentialsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_resend_email_api_v2_users_resend_email_post**
> object user_resend_email_api_v2_users_resend_email_post(user_resend_email_options)

User Resend Email

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    user_resend_email_options = openapi_client.UserResendEmailOptions() # UserResendEmailOptions | 

    try:
        # User Resend Email
        api_response = api_instance.user_resend_email_api_v2_users_resend_email_post(user_resend_email_options)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->user_resend_email_api_v2_users_resend_email_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_resend_email_options** | [**UserResendEmailOptions**](UserResendEmailOptions.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_server_session_token_api_v2_users_server_session_token_post**
> ServersessiontokenResponse user_server_session_token_api_v2_users_server_session_token_post()

User Server Session Token

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    
    try:
        # User Server Session Token
        api_response = api_instance.user_server_session_token_api_v2_users_server_session_token_post()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->user_server_session_token_api_v2_users_server_session_token_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ServersessiontokenResponse**](ServersessiontokenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **user_verify_api_v2_users_verify_token_get**
> object user_verify_api_v2_users_verify_token_get(token)

User Verify

Endpoint for verifying user emails

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    token = 'token_example' # str | 

    try:
        # User Verify
        api_response = api_instance.user_verify_api_v2_users_verify_token_get(token)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DefaultApi->user_verify_api_v2_users_verify_token_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate_cluster_api_v2_sessions_validate_cluster_post**
> validate_cluster_api_v2_sessions_validate_cluster_post(body)

Validate Cluster

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    body = None # object | 

    try:
        # Validate Cluster
        api_instance.validate_cluster_api_v2_sessions_validate_cluster_post(body)
    except ApiException as e:
        print("Exception when calling DefaultApi->validate_cluster_api_v2_sessions_validate_cluster_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_reset_password_token_api_v2_users_reset_password_token_get**
> verify_reset_password_token_api_v2_users_reset_password_token_get(token)

Verify Reset Password Token

Verifies that the specified token is a valid, non-expired password reset token.

### Example

```python
from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    token = 'token_example' # str | 

    try:
        # Verify Reset Password Token
        api_instance.verify_reset_password_token_api_v2_users_reset_password_token_get(token)
    except ApiException as e:
        print("Exception when calling DefaultApi->verify_reset_password_token_api_v2_users_reset_password_token_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

