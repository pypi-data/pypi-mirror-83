from .. import constants
import re
import hashlib

import os,datetime,logging
l = logging.getLogger('ppssauth')

def checkPassword(user,newpassword):
  prevpasslist = user.passowrdhistory
  passworddig = getPasswordDigest(newpassword)
  for prevpass in prevpasslist[0:constants.Conf.passwordpreviousdifferent]:
    l.debug("\n{}\n vs \n{}".format(passworddig, prevpass.password))
    if passworddig == prevpass.password:
      l.warn("password already used at {}".format(prevpass.insertdt))
      return False
  for reexp in constants.Conf.passwordrelist:
    myre = re.compile(reexp)
    if myre.search(newpassword) is None:
      return False
  return True


def getPasswordDigest(password):
  s = hashlib.sha512(password.encode('utf-8'))
  dig = s.hexdigest()
  return dig



