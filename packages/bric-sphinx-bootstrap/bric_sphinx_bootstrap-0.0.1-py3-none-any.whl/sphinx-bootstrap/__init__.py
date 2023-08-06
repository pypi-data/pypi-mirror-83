from sphinx import addnodes
from docutils.nodes import inline, emphasis
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

	node = emphasis( **options )

	return [], []



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

	node = inline( **options )

	return [ node ], []


class BtnPrimary( Directive ):
	"""

	"""
	has_content = True

	def run( self ):
		"""

		"""
		options = { 'classes': [] }
		options[ 'classes' ].append( 'btn' )
		options[ 'classes' ].append( 'btn-sm' )
		options[ 'classes' ].append( 'btn-primary' )

		set_classes( options )
		node = emphasis( **options )

		return [ node ] 


prolog = '.. |btn_primary| btn_primary:: btn_primary\n'

def setup( app ):
	"""
	
	"""

	app.add_role( 'btn_primary', btn_primary_role )
	app.add_role( 'btn_success', btn_success_role )

	app.add_directive( 'btn_primary', BtnPrimary )

	app.config.rst_prolog = prolog
	return { 'version': '0.0.1' }