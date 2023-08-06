"""
Miva Merchant

This file and the source codes contained herein are the property of
Miva, Inc.  Use of this file is restricted to the specific terms and
conditions in the License Agreement associated with this file.  Distribution
of this file or portions of this file for uses not covered by the License
Agreement is not allowed without a written agreement signed by an officer of
Miva, Inc.

Copyright 1998-2020 Miva, Inc.  All rights reserved.
https://www.miva.com

Prefix         : MMT-EXCEPTIONS-
Next Error Code: 1
"""


class Error( Exception ):
	def __init__( self, error_code: str, error_message: str ):
		super().__init__( f'{error_code}: {error_message}' )

		self._error_code	= error_code
		self._error_message	= error_message

	@property
	def error_code( self ):
		return self._error_code

	@property
	def error_message( self ):
		return self._error_message


class ErrorList( Error ):
	def __init__( self, error_code: str, error_message: str, errors: [ str ] ):
		built_error_message = error_message + ':'

		for error in errors:
			built_error_message += f'\n\t{error}'

		super().__init__( error_code, built_error_message )


class APIRequestError( Error ):
	def __init__( self, function: str, error_code: str, error_message: str ):
		super().__init__( error_code, f'{function}: {error_message}' )
