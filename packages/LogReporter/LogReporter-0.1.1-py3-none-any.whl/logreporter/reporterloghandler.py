import logging
from pathlib import Path

class ReporterLogHandler(logging.FileHandler):
  """
  Log handler for Reporter processing.
  """

  def __init__(self, filename=None):
    """
    Constructor.

    Parameters
    ----
    filename: Path or str
      Log file name. If omitted, it will be created in the same folder as the module file.
    """
    # Place the log file in the same folder as the application or directly under the user folder.
    self._filename = Path(__file__).parent / "reporter.log" if filename is None else filename
    super().__init__(self._filename, encoding="utf-8", delay=True)
    self.level == logging.WARNING
    self._enabled = True

  @property
  def enabled(self):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    return self._enabled

  @enabled.setter
  def enabled(self, value):
    """
    Whether to perform log collection processing. If False is set, log collection will be stopped and all accumulated logs will be deleted.
    """
    self._enabled = value
    if not value:
      self.clear()

  @property
  def has_text(self):
    """
    Check if the log text exists.
    """
    return self._filename.exists() and self._filename.stat().st_size > 0

  def emit(self, record):
    """
    Override method.
    If the value of enabled is False, no processing is performed.
    """
    if self.enabled:
      super().emit(record)

  def clear(self):
    """
    Delete all the log text of the actual acquisition.
    """
    with open(self._filename, mode="w", encoding="utf-8") as f:
      f.write("")

  def get_text(self, max_length=-1, report=None):
    """
    Get all the log strings written so far.

    Parameters
    ----
    max_length: int
      Maximum number of characters requested.
      If this value is set, get the text with the number of lines closest to this number of characters and return it.
      Also, in this case, the unacquired text is saved in the internal log file.
      If 1 or 0 is set for this value, ValueError will occur.
    report: func(text) -> bool or None
      A function for reporting.
      If you set a function object here, this function will be called just before extracting the log text and saving the extracted text.
      The character string itself extracted from the log is stored as a parameter.

      The function also returns a bool value as a return value.
      If false is returned, it is considered as a report failure and the text extraction process is not committed.

    Returns
    ----
    text: str
      Log string.
    """
    if max_length == 0 or max_length == 1:
      raise ValueError("The value of max_length is out of range.")
    self.close()
    text = ""
    if self._filename.exists():
      with open(self._filename, mode="r", encoding="utf-8") as f:
        text = f.read()
      if max_length != -1:
        lines = text.splitlines()
        result = []
        if len(lines[0]) > max_length:
          text = lines[0][:max_length]
          lines[0] = lines[0][max_length:]
        else:
          while max_length > 0 and len(lines) > 0:
            t = lines[0]
            max_length -= len(t)
            if max_length >= 0:
              result.append(t)
              lines.pop(0)
              max_length -= len("\n") # Newline character.
          text = "\n".join(result)
        if report is None or report(text):
          with open(self._filename, mode="w", encoding="utf-8") as f:
            f.write("\n".join(lines))
      else:
        if report is None or report(text):
          self.clear()
    return text
