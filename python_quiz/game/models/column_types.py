from sqlalchemy.ext.mutable import Mutable


class MutableList(Mutable, list):
  """
  Specific to PostgreSQL, this allows a column
  to store a mutable list
  """
  def append(self, value):
    list.append(self, value)
    self.changed()

  def extend(self, value):
    list.extend(self, value)
    self.changed()

  def pop(self, index=-1):
    value = list.pop(self, index)
    self.changed()
    return value

  @classmethod
  def coerce(cls, key, value):
    if not isinstance(value, MutableList):
      if isinstance(value, list):
        return MutableList(value)
      return Mutable.coerce(key, value)
    else:
      return value
