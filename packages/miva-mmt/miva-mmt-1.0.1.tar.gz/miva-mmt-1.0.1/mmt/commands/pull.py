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

Prefix         : MMT-COMMAND-PULL-
Next Error Code: 6
"""

import typing

import merchantapi.model
import merchantapi.request

from mmt.exceptions import Error, ErrorList
from mmt.commands import ConfiguredCommand
from mmt.metadata.state import StateMetadataEntryFile, StateMetadataTemplateFile, StateMetadataTemplateSettingsFile, StateMetadataPropertyTemplateFile, StateMetadataPropertySettingsFile, StateMetadataJSResourceJSFile, StateMetadataJSResourceTemplateFile, StateMetadataJSResourceSettingsFile, StateMetadataCSSResourceCSSFile, StateMetadataCSSResourceTemplateFile, StateMetadataCSSResourceSettingsFile, StateMetadataResourceGroupSettingsFile
from mmt.file import File, BinaryFile


class PullCommand( ConfiguredCommand ):
	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )

		self._added_files		= []
		self._updated_files		= []
		self._deleted_files		= []

	def initialize( self ):
		self.ensure_toplevel_directories_exist()

	def run( self ):
		filepaths				= set( filepath for filepath in self.args.get( 'filepaths' ) )
		modified_files			= self.load_modified_files( filtered_filepaths = filepaths )
		out_of_sync_files		= []
		template_filenames		= []
		property_types_codes	= []
		jsresource_codes		= []
		cssresource_codes		= []
		resourcegroup_codes		= []

		# Check to see if any of the locally modified files are explicitly being updated
		if not self.args.get( 'force' ):
			for filepath in filepaths:
				for state_file, file in modified_files:
					if state_file.filepath == filepath:
						out_of_sync_files.append( state_file )

			if len( out_of_sync_files ):
				raise ErrorList( 'MMT-COMMAND-PULL-00001', 'Update failed as the following files contain local modifications', [ out_of_sync_file.filepath for out_of_sync_file in out_of_sync_files ] )

		# If specific files are being updated, the associated requests
		# can be filtered to include only the necessary files
		for filepath in filepaths:
			state_file = self.state.filemanager.lookup( filepath )

			if state_file is not None:
				if state_file.is_template():
					template_filenames.append( state_file.template_filename )
				elif state_file.is_property():
					property_types_codes.append( ( state_file.property_type, state_file.property_code ) )
				elif state_file.is_jsresource():
					jsresource_codes.append( state_file.jsresource_code )
				elif state_file.is_cssresource():
					cssresource_codes.append( state_file.cssresource_code )
				elif state_file.is_resourcegroup():
					resourcegroup_codes.append( state_file.resourcegroup_code )

		changeset							= self._load_changeset( self.args.get( 'c', 0 ) )
		branchtemplateversions				= self._listload_branchtemplateversions( changeset, template_filenames )
		branchpropertyversions				= self._listload_branchpropertyversions( changeset, property_types_codes )
		branchjavascriptresourceversions	= self._listload_branchjavascriptresourceversions( changeset, jsresource_codes )
		branchcssresourceversions			= self._listload_branchcssresourceversions( changeset, cssresource_codes )
		resourcegroups						= self._listload_resourcegroups( changeset, resourcegroup_codes )

		modified_template_files				= self.group_modified_template_files( modified_files )
		modified_property_files				= self.group_modified_property_files( modified_files )
		modified_jsresource_files			= self.group_modified_jsresource_files( modified_files )
		modified_cssresource_files			= self.group_modified_cssresource_files( modified_files )
		modified_resourcegroup_files		= self.group_modified_resourcegroup_files( modified_files )

		# Pull the source from the server and see if any of locally modified files are out-of-sync
		if not self.args.get( 'force' ):
			for state_file, file in modified_template_files:
				for branchtemplateversion in branchtemplateversions:
					if self.template_equals_branchtemplateversion( state_file, branchtemplateversion ):
						if state_file.is_template_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchtemplateversion_template_data( branchtemplateversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_template_settings_file():
							if state_file.sha256_hash is None and not self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
								out_of_sync_files.append( state_file )
							elif state_file.sha256_hash != self.calculate_sha256( self.get_branchtemplateversion_template_settings_data( branchtemplateversion ) ):
								out_of_sync_files.append( state_file )

						break

			for state_file, file in modified_property_files:
				for branchpropertyversion in branchpropertyversions:
					if self.property_equals_branchpropertyversion( state_file, branchpropertyversion ):
						if state_file.is_property_template_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchpropertyversion_template_data( branchpropertyversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_property_settings_file():
							if state_file.sha256_hash is None and not self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
								out_of_sync_files.append( state_file )
							elif state_file.sha256_hash != self.calculate_sha256( self.get_branchpropertyversion_settings_data( branchpropertyversion ) ):
								out_of_sync_files.append( state_file )

						break

			for state_file, file in modified_jsresource_files:
				for branchjavascriptresourceversion in branchjavascriptresourceversions:
					if self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
						if state_file.is_jsresource_settings_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchjavascriptresourceversion_settings_data( branchjavascriptresourceversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_jsresource_js_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchjavascriptresourceversion_local_data( branchjavascriptresourceversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_jsresource_template_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchjavascriptresourceversion_inline_data( branchjavascriptresourceversion ) ):
								out_of_sync_files.append( state_file )

						break

			for state_file, file in modified_cssresource_files:
				for branchcssresourceversion in branchcssresourceversions:
					if self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
						if state_file.is_cssresource_settings_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchcssresourceversion_settings_data( branchcssresourceversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_cssresource_css_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchcssresourceversion_local_data( branchcssresourceversion ) ):
								out_of_sync_files.append( state_file )
						elif state_file.is_cssresource_template_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_branchcssresourceversion_inline_data( branchcssresourceversion ) ):
								out_of_sync_files.append( state_file )

						break

			for state_file, file in modified_resourcegroup_files:
				for resourcegroup in resourcegroups:
					if self.resourcegroup_equals_resourcegroup( state_file, resourcegroup ):
						if state_file.is_resourcegroup_settings_file():
							if state_file.sha256_hash != self.calculate_sha256( self.get_resourcegroup_settings_data( resourcegroup ) ):
								out_of_sync_files.append( state_file )

						break

			if len( out_of_sync_files ) > 0:
				raise ErrorList( 'MMT-COMMAND-PULL-00004', 'Update failed as the following files are out-of-sync with the server and contain local modifications', [ out_of_sync_file.filepath for out_of_sync_file in out_of_sync_files ] )

		"""
		Iterate and delete all current state file entries that
		no longer exist on the server.  This must be done before
		processing any other records in case a file was deleted
		and re-created with the same name.

		In addition, the state files array needs to be copied
		so the iteration of this array will not be affected by
		the removing of state files in the original array.
		"""

		for state_file in self.state.filemanager.files.copy():
			found = False

			if state_file.is_template():
				for branchtemplateversion in branchtemplateversions:
					if self.template_equals_branchtemplateversion( state_file, branchtemplateversion ):
						found = True
						break
			elif state_file.is_property():
				for branchpropertyversion in branchpropertyversions:
					if self.property_equals_branchpropertyversion( state_file, branchpropertyversion ):
						found = True
						break
			elif state_file.is_jsresource():
				for branchjavascriptresourceversion in branchjavascriptresourceversions:
					if self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
						found = True
						break
			elif state_file.is_cssresource():
				for branchcssresourceversion in branchcssresourceversions:
					if self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
						found = True
						break
			elif state_file.is_resourcegroup():
				for resourcegroup in resourcegroups:
					if self.resourcegroup_equals_resourcegroup( state_file, resourcegroup ):
						found = True
						break
			else:
				raise Error( 'MMT-COMMAND-PULL-00005', 'Unknown state file' )

			if not found:
				# Only delete the state file if no filepaths were specified
				# or if the state file was in the list of specific filepaths to
				# be updated

				if len( filepaths ) == 0 or state_file.filepath in filepaths:
					self._deleted_files.append( state_file )
					self.state.filemanager.delete( state_file )

		# Begin updating all record types
		for branchtemplateversion in branchtemplateversions:
			self._process_branchtemplateversion( branchtemplateversion )

		for branchpropertyversion in branchpropertyversions:
			self._process_branchpropertyversion( branchpropertyversion )

		for branchjavascriptresourceversion in branchjavascriptresourceversions:
			self._process_branchjavascriptresourceversion( branchjavascriptresourceversion )

		for branchcssresourceversion in branchcssresourceversions:
			self._process_branchcssresourceversion( branchcssresourceversion )

		for resourcegroup in resourcegroups:
			self._process_resourcegroup( resourcegroup )

		if len( self._added_files ) + len( self._updated_files ) + len( self._deleted_files ) == 0:
			print( 'No files updated' )
		else:
			for state_file in self._added_files:
				print( f'\tAdded: {state_file.filepath}' )

			for state_file in self._updated_files:
				print( f'\tUpdated: {state_file.filepath}' )

			for state_file in self._deleted_files:
				print( f'\tDeleted: {state_file.filepath}' )

		self.state.changeset.id			= changeset.get_id()
		self.state.changeset.username	= changeset.get_user_name()
		self.state.changeset.notes		= changeset.get_notes()
		self.state.save()

	def _load_changeset( self, changeset_id: int ) -> merchantapi.model.Changeset:
		request = merchantapi.request.ChangesetListLoadQuery()
		request.set_branch_id( self.configmanager.branch_id )

		if changeset_id > 0:
			request.set_filters( request.filter_expression().equal( 'id', changeset_id ) )
		else:
			request.set_count( 1 )
			request.set_sort( 'id', request.SORT_DESCENDING )

		response = self.send_request( request )

		if len( response.get_changesets() ) == 0:
			if changeset_id == 0:
				raise Error( 'MMT-COMMAND-PULL-00002', 'No changesets exist' )
			else:
				raise Error( 'MMT-COMMAND-PULL-00003', f'Changeset {changeset_id} does not exist' )

		return response.get_changesets()[ 0 ]

	def _listload_branchtemplateversions( self, changeset: merchantapi.model.Changeset, template_filenames: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchTemplateVersion ]:
		request = merchantapi.request.BranchTemplateVersionListLoadQuery()
		filters = request.filter_expression()

		if len( template_filenames ) > 0:
			filters.is_in( 'filename', template_filenames )
		else:
			filters.equal( 'prop_id', 0 )

			if self.configmanager.ignore_unsynced_templates:
				filters.and_is_true( 'sync' )

		request.set_filters( filters )
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'settings' ] )

		return self.send_request_base64( request ).get_branch_template_versions()

	def _listload_branchpropertyversions( self, changeset: merchantapi.model.Changeset, property_types_codes: typing.List[ typing.Tuple[ str, str ] ] ) -> typing.List[ merchantapi.model.BranchPropertyVersion ]:
		request = merchantapi.request.BranchPropertyVersionListLoadQuery()
		filters = request.filter_expression()

		if len( property_types_codes ) > 0:
			for property_type, property_code in property_types_codes:
				filters.or_x( request.filter_expression().equal( 'type', property_type ).and_equal( 'code', property_code ) )
		else:
			if self.configmanager.ignore_unsynced_properties:
				filters.and_is_true( 'sync' )

		request.set_filters( filters )
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'settings', 'category', 'product' ] )

		return self.send_request_base64( request ).get_branch_property_versions()

	def _listload_branchjavascriptresourceversions( self, changeset: merchantapi.model.Changeset, jsresource_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchJavaScriptResourceVersion ]:
		request = merchantapi.request.BranchJavaScriptResourceVersionListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'linkedpages', 'linkedresources' ] )

		if len( jsresource_codes ) > 0:
			request.set_filters( request.filter_expression().is_in( 'code', jsresource_codes ) )

		return self.send_request_base64( request ).get_branch_java_script_resource_versions()

	def _listload_branchcssresourceversions( self, changeset: merchantapi.model.Changeset, cssresource_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.BranchCSSResourceVersion ]:
		request = merchantapi.request.BranchCSSResourceVersionListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'source', 'linkedpages', 'linkedresources' ] )

		if len( cssresource_codes ) > 0:
			request.set_filters( request.filter_expression().is_in( 'code', cssresource_codes ) )

		return self.send_request_base64( request ).get_branch_css_resource_versions()

	def _listload_resourcegroups( self, changeset: merchantapi.model.Changeset, resourcegroup_codes: typing.List[ str ] ) -> typing.List[ merchantapi.model.ResourceGroup ]:
		request = merchantapi.request.ResourceGroupListLoadQuery()
		request.set_changeset_id( changeset.get_id() )
		request.set_branch_id( self.configmanager.branch_id )
		request.set_on_demand_columns( [ 'linkedjavascriptresources', 'linkedcssresources' ] )

		if len( resourcegroup_codes ) > 0:
			request.set_filters( request.filter_expression().is_in( 'code', resourcegroup_codes ) )

		return self.send_request( request ).get_resource_groups()

	def _process_branchtemplateversion( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ):
		state_file, file	= self._lookup_template_state_file( branchtemplateversion )
		template_data		= self.get_branchtemplateversion_template_data( branchtemplateversion )

		if state_file is None:
			template_filepath		= self.build_template_filepath( branchtemplateversion )
			template_filename		= self.get_branchtemplateversion_filename( branchtemplateversion )
			state_file, file		= self.state.filemanager.add_template( template_filepath, template_filename )

			self._process_lowlevel_add( state_file, file, template_data )
		else:
			if state_file.sha256_hash != self.calculate_sha256( template_data ):
				self._process_lowlevel_update( state_file, file, template_data )

		if branchtemplateversion.get_parent_id() == 0:
			state_file, file		= self._lookup_template_settings_state_file( branchtemplateversion )
			template_settings_data	= self.get_branchtemplateversion_template_settings_data( branchtemplateversion )

			if state_file is None:
				template_settings_filepath	= self.build_template_settings_filepath( branchtemplateversion )
				template_settings_filename	= self.get_branchtemplateversion_filename( branchtemplateversion )
				state_file, file			= self.state.filemanager.add_template( template_settings_filepath, template_settings_filename )

				if not self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
					self._process_lowlevel_add( state_file, file, template_settings_data )
			else:
				if state_file.sha256_hash is None:
					if not self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
						self._process_lowlevel_update( state_file, file, template_settings_data )
				else:
					if self.is_branchtemplateversion_template_settings_empty( branchtemplateversion ):
						self._process_lowlevel_delete( state_file, file )
					elif state_file.sha256_hash != self.calculate_sha256( template_settings_data ):
						self._process_lowlevel_update( state_file, file, template_settings_data )

	def _process_branchpropertyversion( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ):
		self.ensure_property_path_exists( branchpropertyversion )

		if branchpropertyversion.get_template_id():
			state_file, file		= self._lookup_property_template_state_file( branchpropertyversion )
			property_template_data	= self.get_branchpropertyversion_template_data( branchpropertyversion )

			if state_file is None:
				property_template_filepath	= self.build_property_template_filepath( branchpropertyversion )
				property_group				= self.get_branchpropertyversion_group( branchpropertyversion )
				property_type				= self.get_branchpropertyversion_type( branchpropertyversion )
				property_code				= self.get_branchpropertyversion_code( branchpropertyversion )
				state_file, file			= self.state.filemanager.add_property( property_template_filepath, property_group, property_type, property_code )

				self._process_lowlevel_add( state_file, file, property_template_data )
			else:
				if state_file.sha256_hash != self.calculate_sha256( property_template_data ):
					self._process_lowlevel_update( state_file, file, property_template_data )

		if branchpropertyversion.get_version_id():
			state_file, file		= self._lookup_property_settings_state_file( branchpropertyversion )
			property_settings_data	= self.get_branchpropertyversion_settings_data( branchpropertyversion )

			if state_file is None:
				property_settings_filepath	= self.build_property_settings_filepath( branchpropertyversion )
				property_group				= self.get_branchpropertyversion_group( branchpropertyversion )
				property_type				= self.get_branchpropertyversion_type( branchpropertyversion )
				property_code				= self.get_branchpropertyversion_code( branchpropertyversion )
				state_file, file			= self.state.filemanager.add_property( property_settings_filepath, property_group, property_type, property_code )

				if not self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
					self._process_lowlevel_add( state_file, file, property_settings_data )
			else:
				if state_file.sha256_hash is None:
					if not self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
						self._process_lowlevel_update( state_file, file, property_settings_data )
				else:
					if self.is_branchpropertyversion_settings_empty( branchpropertyversion ):
						self._process_lowlevel_delete( state_file, file )
					elif state_file.sha256_hash != self.calculate_sha256( property_settings_data ):
						self._process_lowlevel_update( state_file, file, property_settings_data )

	def _process_branchjavascriptresourceversion( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ):
		# Always create / update the settings file
		state_file, file			= self._lookup_jsresource_settings_state_file( branchjavascriptresourceversion )
		jsresource_settings_data	= self.get_branchjavascriptresourceversion_settings_data( branchjavascriptresourceversion )

		if state_file is None:
			jsresource_settings_filepath	= self.build_jsresource_settings_filepath( branchjavascriptresourceversion )
			jsresource_settings_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
			state_file, file				= self.state.filemanager.add_jsresource( jsresource_settings_filepath, jsresource_settings_code )

			self._process_lowlevel_add( state_file, file, jsresource_settings_data )
		else:
			if state_file.sha256_hash != self.calculate_sha256( jsresource_settings_data ):
				self._process_lowlevel_update( state_file, file, jsresource_settings_data )

		# Add / update the local file
		if branchjavascriptresourceversion.get_type() == 'L':
			state_file, file		= self._lookup_jsresource_js_state_file( branchjavascriptresourceversion )
			jsresource_local_data	= self.get_branchjavascriptresourceversion_local_data( branchjavascriptresourceversion )

			if state_file is None:
				jsresource_local_filepath	= self.build_jsresource_local_filepath( branchjavascriptresourceversion )
				jsresource_local_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
				state_file, file			= self.state.filemanager.add_jsresource( jsresource_local_filepath, jsresource_local_code )

				self._process_lowlevel_add( state_file, file, jsresource_local_data )
			else:
				if state_file.sha256_hash != self.calculate_sha256( jsresource_local_data ):
					self._process_lowlevel_update( state_file, file, jsresource_local_data )

		# Add / update the template file
		if branchjavascriptresourceversion.get_type() == 'I':
			state_file, file		= self._lookup_jsresource_template_state_file( branchjavascriptresourceversion )
			jsresource_inline_data	= self.get_branchjavascriptresourceversion_inline_data( branchjavascriptresourceversion )

			if state_file is None:
				jsresource_inline_filepath	= self.build_jsresource_inline_filepath( branchjavascriptresourceversion )
				jsresource_inline_code		= self.get_branchjavascriptresourceversion_code( branchjavascriptresourceversion )
				state_file, file			= self.state.filemanager.add_jsresource( jsresource_inline_filepath, jsresource_inline_code )

				self._process_lowlevel_add( state_file, file, jsresource_inline_data )
			else:
				if state_file.sha256_hash != self.calculate_sha256( jsresource_inline_data ):
					self._process_lowlevel_update( state_file, file, jsresource_inline_data )

	def _process_branchcssresourceversion( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ):
		# Always create / update the settings file
		state_file, file			= self._lookup_cssresource_settings_state_file( branchcssresourceversion )
		cssresource_settings_data	= self.get_branchcssresourceversion_settings_data( branchcssresourceversion )

		if state_file is None:
			cssresource_settings_filepath	= self.build_cssresource_settings_filepath( branchcssresourceversion )
			cssresource_settings_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
			state_file, file				= self.state.filemanager.add_cssresource( cssresource_settings_filepath, cssresource_settings_code )

			self._process_lowlevel_add( state_file, file, cssresource_settings_data )
		else:
			if state_file.sha256_hash != self.calculate_sha256( cssresource_settings_data ):
				self._process_lowlevel_update( state_file, file, cssresource_settings_data )

		# Add / update the local file
		if branchcssresourceversion.get_type() == 'L':
			state_file, file		= self._lookup_cssresource_css_state_file( branchcssresourceversion )
			cssresource_local_data	= self.get_branchcssresourceversion_local_data( branchcssresourceversion )

			if state_file is None:
				cssresource_local_filepath	= self.build_cssresource_local_filepath( branchcssresourceversion )
				cssresource_local_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
				state_file, file			= self.state.filemanager.add_cssresource( cssresource_local_filepath, cssresource_local_code )

				self._process_lowlevel_add( state_file, file, cssresource_local_data )
			else:
				if state_file.sha256_hash != self.calculate_sha256( cssresource_local_data ):
					self._process_lowlevel_update( state_file, file, cssresource_local_data )

		# Add / update the template file
		if branchcssresourceversion.get_type() == 'I':
			state_file, file		= self._lookup_cssresource_template_state_file( branchcssresourceversion )
			cssresource_inline_data	= self.get_branchcssresourceversion_inline_data( branchcssresourceversion )

			if state_file is None:
				cssresource_inline_filepath	= self.build_cssresource_inline_filepath( branchcssresourceversion )
				cssresource_inline_code		= self.get_branchcssresourceversion_code( branchcssresourceversion )
				state_file, file			= self.state.filemanager.add_cssresource( cssresource_inline_filepath, cssresource_inline_code )

				self._process_lowlevel_add( state_file, file, cssresource_inline_data )
			else:
				if state_file.sha256_hash != self.calculate_sha256( cssresource_inline_data ):
					self._process_lowlevel_update( state_file, file, cssresource_inline_data )

	def _process_resourcegroup( self, resourcegroup: merchantapi.model.ResourceGroup ):
		state_file, file			= self._lookup_resourcegroup_settings_state_file( resourcegroup )
		resourcegroup_settings_data	= self.get_resourcegroup_settings_data( resourcegroup )

		if state_file is None:
			resourcegroup_settings_filepath	= self.build_resourcegroup_settings_filepath( resourcegroup )
			resourcegroup_settings_code		= self.get_resourcegroup_code( resourcegroup )
			state_file, file				= self.state.filemanager.add_resourcegroup( resourcegroup_settings_filepath, resourcegroup_settings_code )

			self._process_lowlevel_add( state_file, file, resourcegroup_settings_data )
		else:
			if state_file.sha256_hash != self.calculate_sha256( resourcegroup_settings_data ):
				self._process_lowlevel_update( state_file, file, resourcegroup_settings_data )

	def _process_lowlevel_add( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ], data: typing.AnyStr ):
		file.write( data )
		state_file.sha256_hash = file.sha256_hash

		self._added_files.append( state_file )

	def _process_lowlevel_update( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ], data: typing.AnyStr ):
		file.write( data )
		state_file.sha256_hash = file.sha256_hash

		self._updated_files.append( state_file )

	def _process_lowlevel_delete( self, state_file: StateMetadataEntryFile, file: typing.Union[ File, BinaryFile ] ):
		file.delete()
		state_file.sha256_hash = None

		self._deleted_files.append( state_file )

	def _lookup_template_state_file( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> typing.Union[ typing.Tuple[ StateMetadataTemplateFile, File ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_template() and state_file.is_template_file() and self.template_equals_branchtemplateversion( state_file, branchtemplateversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_template_settings_state_file( self, branchtemplateversion: merchantapi.model.BranchTemplateVersion ) -> typing.Union[ typing.Tuple[ StateMetadataTemplateSettingsFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_template() and state_file.is_template_settings_file() and self.template_equals_branchtemplateversion( state_file, branchtemplateversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_property_template_state_file( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> typing.Union[ typing.Tuple[ StateMetadataPropertyTemplateFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_property() and state_file.is_property_template_file() and self.property_equals_branchpropertyversion( state_file, branchpropertyversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_property_settings_state_file( self, branchpropertyversion: merchantapi.model.BranchPropertyVersion ) -> typing.Union[ typing.Tuple[ StateMetadataPropertySettingsFile, File ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_property() and state_file.is_property_settings_file() and self.property_equals_branchpropertyversion( state_file, branchpropertyversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_jsresource_settings_state_file( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataJSResourceSettingsFile, File ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_jsresource() and state_file.is_jsresource_settings_file() and self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_jsresource_js_state_file( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataJSResourceJSFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_jsresource() and state_file.is_jsresource_js_file() and self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_jsresource_template_state_file( self, branchjavascriptresourceversion: merchantapi.model.BranchJavaScriptResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataJSResourceTemplateFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_jsresource() and state_file.is_jsresource_template_file() and self.jsresource_equals_branchjavascriptresourceversion( state_file, branchjavascriptresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_cssresource_settings_state_file( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataCSSResourceSettingsFile, File ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_cssresource() and state_file.is_cssresource_settings_file() and self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_cssresource_css_state_file( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataCSSResourceCSSFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_cssresource() and state_file.is_cssresource_css_file() and self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_cssresource_template_state_file( self, branchcssresourceversion: merchantapi.model.BranchCSSResourceVersion ) -> typing.Union[ typing.Tuple[ StateMetadataCSSResourceTemplateFile, BinaryFile ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_cssresource() and state_file.is_cssresource_template_file() and self.cssresource_equals_branchcssresourceversion( state_file, branchcssresourceversion ):
				return state_file, state_file.file

		return None, None

	def _lookup_resourcegroup_settings_state_file( self, resourcegroup: merchantapi.model.ResourceGroup ) -> typing.Union[ typing.Tuple[ StateMetadataResourceGroupSettingsFile, File ], typing.Tuple[ None, None ] ]:
		for state_file in self.state.filemanager.files:
			if state_file.is_resourcegroup() and state_file.is_resourcegroup_settings_file() and self.resourcegroup_equals_resourcegroup( state_file, resourcegroup ):
				return state_file, state_file.file

		return None, None
