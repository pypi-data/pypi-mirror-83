[![codecov](https://codecov.io/gh/Vantiv/cnp-chargeback-sdk-python/branch/2.x/graph/badge.svg)](https://codecov.io/gh/Vantiv/cnp-chargeback-sdk-python/branch/2.x) ![Github All Releases](https://img.shields.io/github/downloads/vantiv/cnp-chargeback-sdk-python/total.svg)
[![GitHub](https://img.shields.io/github/license/vantiv/cnp-chargeback-sdk-python.svg)](https://github.com/Vantiv/cnp-chargeback-sdk-python/2.x/LICENSE) 
[![GitHub issues](https://img.shields.io/github/issues/vantiv/cnp-chargeback-sdk-python.svg)](https://github.com/Vantiv/cnp-chargeback-sdk-python/issues)

Vantiv eCommerce Python Chargeback SDK
=====================

About Vantiv eCommerce
------------
[Vantiv eCommerce](https://developer.vantiv.com/community/ecommerce) powers the payment processing engines for leading companies that sell directly to consumers through  internet retail, direct response marketing (TV, radio and telephone), and online services. Vantiv eCommerce is the leading authority in card-not-present (CNP) commerce, transaction processing and merchant services.


About this SDK
--------------
The Vantiv eCommerce Python Chargeback SDK is a Python implementation of the [Vantiv eCommerce](https://developer.vantiv.com/community/ecommerce) Chargeback API. This SDK was created to make it as easy as possible to manage your chargebacks using Vantiv eCommerce API. This SDK utilizes the HTTPS protocol to securely connect to Vantiv eCommerce. Using the SDK requires coordination with the Vantiv eCommerce team in order to be provided with credentials for accessing our systems.

Each Python SDK release supports all of the functionality present in the associated Vantiv eCommerce Chargeback API version (e.g., SDK v2.1.0 supports Vantiv eCommerce Chargeback API v2.1). Please see the Chargeback API reference guide to get more details on what the Vantiv eCommerce chargeback engine supports.

This SDK was implemented to support the Python programming language and was created by Vantiv eCommerce. Its intended use is for online and batch transaction processing utilizing your account on the Vantiv eCommerce payments engine.

See LICENSE file for details on using this software.

Please contact [Vantiv eCommerce](https://developer.vantiv.com/community/ecommerce) to receive valid merchant credentials in order to run tests successfully or if you require assistance in any way.  We are reachable at sdksupport@Vantiv.com

Dependencies
------------
* pyxb v1.2.5 : http://pyxb.sourceforge.net/
* paramiko v1.14.0: http://www.paramiko.org/
* requests v2.13.0: http://docs.python-requests.org/en/master/
* six v1.10.0: https://github.com/benjaminp/six
* xmltodict 0.10.2: https://github.com/martinblech/xmltodict

Setup
-----
1) To download and install:

Using pip 

>pip install CnpChargebackSdk

Without Pip

>git clone https://github.com/Vantiv/cnp-chargeback-sdk-python.git

>cd cnp-chargeback-sdk-python

checkout branch master for XML v2.x
>git checkout master

>python setup.py install

2) setup configurations

>cnp_chargeback_sdk_setup

3) Create a python file similar to:

```python
#Example for Chargeback SDK
from __future__ import print_function, unicode_literals

from cnpsdk import *

# Initial Configuration object. If you have saved configuration in '.vantiv_chargeback_sdk.conf' at system environment
# variable: CHARGEBACK_SDK_CONFIG or user home directory, the saved configuration will be automatically load.
conf = utils.Configuration()

# Configuration need following attributes for chargeback requests:
# user = ''
# password = ''
# merchantId = ''
# url = 'https://www.testvantivcnp.com/sandbox/communicator/online'
# proxy = ''

# Retrieving information about a chargeback by caseId:
response = chargeback_retrieval.get_chargeback_by_case_id(xxxx)
response = chargeback_retrieval.get_chargebacks_by_date("2018-01-01)

# Update chargeback case
chargeback_update.represent_case(xxxx, "Note on activity: represented case!")
chargeback_update.assign_case_to_user(xxxx, "userId", "Note on activity: assigned case to user!")

# Upload and manage documents to support chargeback case
chargeback_docuemnt.upload_document(xxxx, "invoice.pdf")
response = chargeback_docuemnt.list_documents(xxxx)

```

Please contact Vantiv eCommerce with any further questions. You can reach us at SDKSupport@Vantiv.com
