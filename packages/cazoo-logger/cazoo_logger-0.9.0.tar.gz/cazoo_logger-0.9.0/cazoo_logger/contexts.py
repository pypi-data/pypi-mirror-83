import logging
from collections import ChainMap


class ContextualAdapter(logging.LoggerAdapter):
    def __init__(self, logger, data=None):
        self.context = data
        super().__init__(logger, data)

    def with_context(self, **ctx):
        new_ctx = self.context.new_child()
        new_ctx.update({"context": ctx})
        return ContextualAdapter(self.logger, new_ctx)

    def with_data(self, **ctx):
        new_ctx = self.context.new_child()
        new_ctx.update({"data": ctx})
        return ContextualAdapter(self.logger, new_ctx)

    def process(self, msg, kwargs):
        if "extra" in kwargs:
            extra = kwargs["extra"].copy()
            del kwargs["extra"]
            kwargs["extra"] = {"data": extra}
            kwargs["extra"].update(self.context)
        else:
            kwargs["extra"] = self.context

        if "type" in kwargs:
            kwargs["extra"]["type"] = kwargs.pop("type")

        return msg, kwargs

    def addFilter(self, filter):
        self.logger.addFilter(filter)


class LambdaContext(ContextualAdapter):
    def __init__(self, context, data, logger, service=None):
        default = {
            "context": {
                "request_id": context.aws_request_id,
                "function": {
                    "name": context.function_name,
                    "version": context.function_version,
                },
            }
        }
        if service is not None:
            default["context"]["function"]["service"] = service
        default["context"].update(data)
        if service is not None:
            default["context"]["function"]["service"] = service
        super().__init__(logger, ChainMap(default))


class S3SnsContext(LambdaContext):
    def __init__(self, event, context, logger, service=None):
        [record] = event["Records"]
        super().__init__(
            context,
            {
                "sns": {
                    "id": record["Sns"]["MessageId"],
                    "type": record["Sns"]["Type"],
                    "topic": record["Sns"]["TopicArn"],
                    "subject": record["Sns"]["Subject"],
                }
            },
            logger,
            service,
        )


class CloudwatchContext(LambdaContext):
    def __init__(self, event, context, logger, service=None):
        super().__init__(
            context,
            {
                "event": {
                    "source": event["source"],
                    "name": event["detail-type"],
                    "id": event["id"],
                }
            },
            logger,
            service,
        )
