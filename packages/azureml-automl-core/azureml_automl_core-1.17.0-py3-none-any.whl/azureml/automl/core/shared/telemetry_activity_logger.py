# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Telemetry activity logger."""
from typing import Any, Dict, Iterator, Optional
from datetime import datetime
import logging
import uuid

from azureml.automl.core.shared import constants as constants
from azureml.automl.core.shared import log_server

from .activity_logger import ActivityLogger


class TelemetryActivityLogger(ActivityLogger):
    """Telemetry activity logger."""

    def _log_activity(self,
                      logger: logging.Logger,
                      activity_name: str,
                      activity_type: Optional[str] = None,
                      custom_dimensions: Optional[Dict[str, Any]] = None) -> Iterator[None]:
        """
        Log activity with duration and status.

        :param logger: logger
        :param activity_name: activity name
        :param activity_type: activity type
        :param custom_dimensions: custom dimensions
        """
        # Circular dependency so this must be imported here.
        # We should remove the logging_utilities wrapper and just rely on a singleton
        # from this module.
        from .logging_utilities import log_traceback
        activity_info = {'activity_id': str(uuid.uuid4()),
                         'activity_name': activity_name,
                         'activity_type': activity_type}  # type: Dict[str, Any]

        with log_server.lock:
            activity_info.update(log_server.custom_dimensions)

        completion_status = constants.TelemetryConstants.SUCCESS

        start_time = datetime.utcnow()
        logger.info("ActivityStarted: {}".format(activity_name), extra={"properties": activity_info})

        try:
            yield
        except Exception as e:
            completion_status = constants.TelemetryConstants.FAILURE
            # Some exceptions might not be serializable so we can wrap log_traceback in this try/catch.
            # If we run into an exception during log_traceback, the new exception will be serializable and
            # safe to log.
            try:
                log_traceback(e, logger)
            except Exception as traceback_exception:
                logger.error("Failed to log exception during {} failure.".format(activity_name))
                log_traceback(traceback_exception, logger)
            # We then want to re-raise the original exception.
            raise
        finally:
            end_time = datetime.utcnow()
            duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)
            activity_info["durationMs"] = duration_ms
            activity_info["completionStatus"] = completion_status

            logger.info("ActivityCompleted: Activity={}, HowEnded={}, Duration={}[ms]".
                        format(activity_name, completion_status, duration_ms),
                        extra={"properties": activity_info})
