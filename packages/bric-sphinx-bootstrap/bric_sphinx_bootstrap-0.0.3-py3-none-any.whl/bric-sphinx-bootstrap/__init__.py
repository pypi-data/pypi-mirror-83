from sphinx import addnodes
from docutils.nodes import inline
from docutils.parsers.rst.roles import set_classes
from docutils.parsers.rst import Directive


def btn_primary_role( 
	role, rawtext, text, lineno, inliner, 
	options = {}, content = [] 
):
	"""

	"""
	options.update( { 'classes': [] } )
	options[ 'classes' ].append( 'btn' )
	options[ 'classes' ].append( 'btn-sm' )
	options[ 'classes' ].append( 'btn-primary' )
	set_classes( options )

	options[ 'text' ] = text

	node = inline( **options )

	return [ node ], []



def btn_success_role(	
	role, rawtext, text, lineno, inliner, 
	options = {}, content = [] 
):
	"""

	"""
	options.update( { 'classes': [] } )
	options[ 'classes' ].append( 'btn' )
	options[ 'classes' ].append( 'btn-sm' )
	options[ 'classes' ].append( 'btn-success' )
	set_classes( options )

	options[ 'text' ] = text


	node = inline( **options )

	return [ node ], []



prolog = '.. |bs_btn_primary| bs_btn_primary:: bs_btn_primary\n'
prolog = '.. |bs_btn_success| bs_btn_success:: bs_btn_success\n'



def setup( app ):
	"""
	
	"""

	app.add_role( 'bs_btn_primary', btn_primary_role )
	app.add_role( 'bs_btn_success', btn_success_role )

	app.config.rst_prolog = prolog
	return { 'version': '0.0.1' }