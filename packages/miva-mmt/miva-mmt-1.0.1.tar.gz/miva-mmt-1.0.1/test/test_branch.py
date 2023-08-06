from mmt.exceptions import Error
from test import MMTTest


class TestBranchGenericValidate( MMTTest ):
	def test_branch_validate( self ):
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', credential_key = 'invalid_credential_key' )

		self.assertEqual( e.exception.error_message, 'Credential key \'invalid_credential_key\' does not exist' )

		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_validate', store_code = '' )

		self.assertEqual( e.exception.error_message, 'A Store Code is required' )


class TestBranchList( MMTTest ):
	def test_branch_list( self ):
		self.branch_delete( 'test_branch_list_1' )
		self.branch_delete( 'test_branch_list_2' )

		self.branch_create( 'test_branch_list_1', color = '#FFFFFF' )
		self.branch_create( 'test_branch_list_2', color = '#000000' )

		data = self.branch_list()

		# Verify specific data
		self.assertIn( 'Branch: test_branch_list_1',	data )
		self.assertIn( 'Branch: test_branch_list_2',	data )

		# Verify generic data
		self.assertIn( 'Is Primary: False', 			data )
		self.assertIn( 'Is Primary: True',				data )
		self.assertIn( 'Is Working: False',				data )
		self.assertIn( 'Is Working: True',				data )
		self.assertIn( 'Preview URL: http',				data )

		branch = self.branch_load_api( 'test_branch_list_1' )
		self.assertEqual( branch.get_color(), '#FFFFFF' )

		branch = self.branch_load_api( 'test_branch_list_2' )
		self.assertEqual( branch.get_color(), '#000000' )


class TestBranchCreate( MMTTest ):
	def test_branch_add( self ):
		with self.assertRaises( Error ) as e:
			self.branch_create( 'test_branch_add', _from = 'invalid' )

		self.assertEqual( e.exception.error_message, 'Branch \'invalid\' does not exist' )

		self.branch_delete( 'test_branch_add' )
		self.branch_create( 'test_branch_add' )
		self.assertIn( 'Branch: test_branch_add', self.branch_list() )

class TestBranchDelete( MMTTest ):
	def test_branch_delete( self ):
		self.branch_delete( 'test_branch_delete' )

		self.branch_create( 'test_branch_delete' )
		self.assertIn( 'Branch: test_branch_delete', self.branch_list() )

		self.branch_delete( 'test_branch_delete' )
		self.assertNotIn( 'Branch: test_branch_delete', self.branch_list() )
