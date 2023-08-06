
import logging

from logreporter.reporterloghandler import ReporterLogHandler

class Reporter(object):
  """
  The main class that reports logs.
  This object has a singleton implementation. Therefore, the same object can always be obtained on one application.
  """
  _instance = None

  def __init__(self, *args, **kwargs):
    pass

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.__initialize(*args, **kwargs)
    return cls._instance

  def __initialize(self):
    """
    A method that behaves as a constructor.
    This method is only executed when there is no instance of this class in the process.
    """
    self._handler = None
    self.logger = None
    self.reporter = None

  def setup(self, logger, reporter, filename=None, format=None, enabled=True, ):
    """
    Set up the Reporter object.

    Parameters
    ----
    logger: logging.Logger
      Logger object.
    reporter: AbstractReporter
      Reporter object.
    filename: Path or str
      Log file name. If omitted, it will be created in the same folder as the module file.
    format: logging.Formatter or str
      Log output format.
    enabled: bool
      A flag that indicates whether to enable log collection. No logs are collected when set to False.
    """
    self._handler = ReporterLogHandler(filename=filename)
    self.setformat(format)
    self.enabled = enabled
    self.logger = logger
    self.reporter = reporter
    logger.addHandler(self._handler)

  def setformat(self, format):
    """
    Set the formatter for this handler.

    Parameters
    ----
    format: logging.Formatter or str
      Log output format.
    """
    if type(format) is logging.Formatter:
      self._handler.setFormatter(format)
    elif type(format) is str:
      self._handler.setFormatter(logging.Formatter(format))

  def upload_report(self, message=""):
    """
    Extract the log and send it.
    The transmission process depends on the reporter object set in `Reporter # setup ()`.

    Parameters
    ----
    message: str
      Additional message when sending logs.

    Returns
    ----
    successful: bool
      A value that indicates whether all logs have been sent. If the log remains, it will be False.
    """
    result = True
    if self.reporter is not None:
      self.reporter.request_report(self._handler, message)
      result = not self._handler.has_text
    return result

  #region properties

  @property
  def enabled(self):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    return self._handler.enabled

  @enabled.setter
  def enabled(self, value):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    self._handler.enabled = value

  @property
  def log_remaining(self):
    """
    Returns a value that indicates whether log data remains.
    """
    return self._handler.has_text

  #endregion

  #region for testing

  @staticmethod
  def reset():
    """
    Destroy an instance of the class and reset all states.
    This method is only used for unit tests.
    """
    Reporter._instance = None

  #endregion
