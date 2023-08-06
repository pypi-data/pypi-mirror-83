# Backend.ai Error Monitoring Plugin with Sentry

## Installation

Just `pip install backend.ai-monitor-sentry` inside the virtualenv of the Backend.AI Manager and Agent.

## Configuration

Set a key with the Sentry DSN string in the cluster's etcd, by running the following command:
```
backend.ai mgr etcd put config/plugins/error_monitor/sentry/dsn "<dsn>"
```
