from abc import abstractmethod

class AbstractReporter(object):
  """
  The base class of the Reporter. This class is inherited and used.
  In response to the log transmission request, the log is actually transmitted.
  """
  @abstractmethod
  def request_report(self, log_handler, message=""):
    """
    Actually send a log message to the upper platform.
    When the method is called, `request_reporter()` uploads the string in the log to the higher platform as much as possible.
    If the upload fails, or if all uploads are not possible, log the data that could not be sent without deleting it.

    Parameters
    ----
    log_handler: ReporterLogHandler
      `ReporterLogHandler` that stores the log.
    message: str
      Optional additional messages.
    """
    raise NotImplementedError
