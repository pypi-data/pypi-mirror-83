#!/usr/bin/env python

"""Tests for `parser201` package."""

import pytest, pickle, os
from parser201.parser201 import LogParser

BENCH = os.path.join(os.path.dirname(__file__),'benchmark.bin')
LOG   = os.path.join(os.path.dirname(__file__),'samplelog.apa')

# Constants - Indices in the tuple for the benchmark results.

IPADDR  = 0
UID     = 1
UNAME   = 2
TIME    = 3
REQUEST = 4
STATUS  = 5
SIZE    = 6
REFER   = 7
UAGENT  = 8
STRVER  = 9

# --------------------------------------------------------------

# Fixture to load files. Indicating scope='module' means the fixture will just
# be called once at the start of the testing sequence, and be will applied to
# all tests that use it. Also, by yielding results (vice returning) we'll turn
# the module-wide fixture into a generator, which will continue until exhausted
# (last test). That means we can tear-down after the yield.

@pytest.fixture(scope='module')
def fileSetup():
   
   # Setup
   
   with open(LOG,'r') as cases:
      L1 = cases.readlines()
   numCases = len(L1)

   with open(BENCH,'rb') as benchmark:
      L2 = pickle.load(benchmark)

   yield L1,L2
   
   # Tear-down would go here
         
# --------------------------------------------------------------
# Tests
# --------------------------------------------------------------
   
# IP address

def test_ip(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).ipaddress == benchmark[IPADDR]
         
# User ID

def test_userid(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).userid == benchmark[UID]

# User Name

def test_username(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).username == benchmark[UNAME]

# Timestamp

def test_timestamp(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).timestamp == benchmark[TIME]

# Request Line

def test_requestline(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).requestline == benchmark[REQUEST]

# Status Code

def test_statuscode(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).statuscode == benchmark[STATUS]

# Data Size

def test_datasize(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).datasize == benchmark[SIZE]

# Referrer

def test_referrer(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).referrer == benchmark[REFER]

# User Agent

def test_useragent(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert LogParser(line).useragent == benchmark[UAGENT]

# Verify operation of the __str__ method

def test_str(fileSetup):
   for line,benchmark in zip(fileSetup[0],fileSetup[1]):
      assert str(LogParser(line)) == benchmark[STRVER]
      
# For complete code coverage, exercise the setter methods.

def test_setters():
   # This should result in an object with all the fields set to None.
   lp = LogParser('test')
   
   lp.ipaddress = '192.168.1.1'
   assert lp.ipaddress == '192.168.1.1'
   
   lp.userid = 'mr-test'
   assert lp.userid == 'mr-test'

   lp.username = 'geozeke'
   assert lp.username == 'geozeke'

   lp.timestamp = '24/Mar/2009:18:07:16 +0100'
   assert lp.timestamp == '24/Mar/2009:18:07:16 +0100'
   
   lp.requestline = 'GET /images/puce.gif HTTP/1.1'
   assert lp.requestline == 'GET /images/puce.gif HTTP/1.1'
   
   lp.statuscode = 404
   assert lp.statuscode == 404

   lp.datasize = 20000
   assert lp.datasize == 20000

   lp.referrer = 'Test referrer'
   assert lp.referrer == 'Test referrer'

   lp.useragent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322)'
   assert lp.useragent == 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB5; .NET CLR 1.1.4322)'

# --------------------------------------------------------------
