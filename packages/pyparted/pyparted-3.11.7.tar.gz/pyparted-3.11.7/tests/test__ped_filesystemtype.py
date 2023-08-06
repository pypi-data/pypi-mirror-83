#
# Copyright (C) 2009-2011  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Chris Lumens <clumens@redhat.com>
#
import _ped
import unittest

# One class per method, multiple tests per class.  For these simple methods,
# that seems like good organization.  More complicated methods may require
# multiple classes and their own test suite.
class FileSystemTypeNewTestCase(unittest.TestCase):
    def runTest(self):
        # You can't create a FileSystemType by hand.
        self.assertRaises(TypeError, _ped.FileSystemType)

class FileSystemTypeGetSetTestCase(unittest.TestCase):
    def runTest(self):
        fstype = _ped.file_system_type_get("ext3")

        self.assertIsInstance(fstype, _ped.FileSystemType)
        self.assertEqual(fstype.name, "ext3")
        self.assertEqual(getattr(fstype, "name"), "ext3")
        self.assertRaises(AttributeError, setattr, fstype, "name", "vfat")
        self.assertRaises(AttributeError, getattr, fstype, "junk")

class FileSystemTypeStrTestCase(unittest.TestCase):
    def runTest(self):
        fstype = _ped.file_system_type_get("ext3")

        self.assertEqual(str(fstype), "_ped.FileSystemType instance --\n  name: ext3")
