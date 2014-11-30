from __future__ import print_function

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic 

from IPython.utils.io import capture_output
from IPython.display import display

from pyOlog import SimpleOlogClient
from pyOlog.utils import save_pyplot_figure, get_screenshot, get_text_from_editor

olog_client = SimpleOlogClient()

def olog(msg = None, logbooks = None, tags = None, 
         attachments = None, **kwargs):
  """Make a log entry to the Olog

  :param msg: Message for log entry. 
              If None use and editor to get message.
  :param logbooks: Logbooks to add message to.
  :type logbooks: String or List of Strings.
  :param tags: Tags to tag the log entry with.
  :type tags: String or List of Strings.
  :param attachments: List of attachments to add to log entry.
  :type attachments: Attchment objects 
  """
  if not msg:
    msg = get_text_from_editor()
  olog_client.log(msg, logbooks = logbooks, tags = tags,
                  attachments = attachments)
  return

def olog_savefig(**kwargs):
  """Save a pyplot figure and place it in tho Olog
  
  The **kwargs are all passed onto the :func savefig: function
  and then onto the :func olog" function
  
  :returns: None
  """ 
  fig = save_pyplot_figure(**kwargs)
  if 'attachments' in kwargs:
    if isinstance(kwargs['attachments'], list):
      kwargs['attachments'].append(fig)
    else:
      kwargs['attachments'] = [kwargs['attatchments'], fig]
  else:
    kwargs['attachments'] = fig

  olog(**kwargs)
  return 

def olog_grab(root = False, **kwargs):
  """Grab a screenshot and place it in tho Olog
  
  :param root" If True, the entire screen is grabbed else select
               an area as a rubber band.

  The **kwargs are all passed onto the :func olog: function
  
  :returns: None
  """ 
  if not root:
    print("Select area of screen to grab .........")
  a = get_screenshot(root)
  if 'attachments' in kwargs:
    if isinstance(kwargs['attachments'], list):
      kwargs['attachments'].append(a)
    else:
      kwargs['attachments'] = [kwargs['attatchments'], a]
  else:
    kwargs['attachments'] = a

  olog(**kwargs)
  return 

@magics_class
class OlogMagics(Magics):
  msg_store = ''

  @line_magic
  def log_add(self, line):
    with capture_output() as c:
      self.shell.run_cell(line)
    c.show()
    self.msg_store += c.stdout
    self.msg_store += '\n'

  @line_magic
  def log_end(self, line):
    text = get_text_from_editor(prepend = self.msg_store) 
    olog_client.log(text)
    self.msg_store = ''

  @line_magic
  def log_clear(self, line):
    self.msg_store = ''

  @line_magic
  def log_line(self, line):
    with capture_output() as c:
      self.shell.run_cell(line)
    c.show()
    msg = c.stdout
    olog_client.log(msg)

  @line_magic
  def logit(self, line):
    if line.strip() == '':
      olog_client.log()
    else:
      olog_cleint.log(msg = line.strip())

  @line_magic
  def grabit(self, line):
    olog_grab()

def load_ipython_extension(ipython):
  push_vars = {'olog'         : olog,
               'olog_savefig' : olog_savefig,
               'olog_grab'    : olog_grab}
  ipython.push(push_vars) 
  ipython.register_magics(OlogMagics)
