class Product:

	Clayful = None
	name = 'Product'
	path = 'products'

	@staticmethod
	def config(clayful):

		Product.Clayful = clayful

		return Product

	@staticmethod
	def list(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/products',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/products/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/products/{productId}',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def create(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'create',
			'http_method':      'POST',
			'path':             '/v1/products',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def create_variant(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'create_variant',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/variants',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_censored(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'mark_as_censored',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/censored',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def create_variation(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'create_variation',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/options/{optionId}/variations',
			'params':           ('productId', 'optionId', ),
			'args':             args
		})

	@staticmethod
	def increase_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'increase_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/inc',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def pull_from_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'pull_from_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/pull',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def push_to_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'push_to_metafield',
			'http_method':      'POST',
			'path':             '/v1/products/{productId}/meta/{field}/push',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def update(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'update',
			'http_method':      'PUT',
			'path':             '/v1/products/{productId}',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def update_option(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'update_option',
			'http_method':      'PUT',
			'path':             '/v1/products/{productId}/options/{optionId}',
			'params':           ('productId', 'optionId', ),
			'args':             args
		})

	@staticmethod
	def update_variant(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'update_variant',
			'http_method':      'PUT',
			'path':             '/v1/products/{productId}/variants/{variantId}',
			'params':           ('productId', 'variantId', ),
			'args':             args
		})

	@staticmethod
	def update_variation(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'update_variation',
			'http_method':      'PUT',
			'path':             '/v1/products/{productId}/options/{optionId}/variations/{variationId}',
			'params':           ('productId', 'optionId', 'variationId', ),
			'args':             args
		})

	@staticmethod
	def delete(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'delete',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def mark_as_uncensored(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'mark_as_uncensored',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}/censored',
			'params':           ('productId', ),
			'args':             args
		})

	@staticmethod
	def delete_variant(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'delete_variant',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}/variants/{variantId}',
			'params':           ('productId', 'variantId', ),
			'args':             args
		})

	@staticmethod
	def delete_metafield(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'delete_metafield',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}/meta/{field}',
			'params':           ('productId', 'field', ),
			'args':             args
		})

	@staticmethod
	def delete_variation(*args):

		return Product.Clayful.call_api({
			'model_name':       Product.name,
			'method_name':      'delete_variation',
			'http_method':      'DELETE',
			'path':             '/v1/products/{productId}/options/{optionId}/variations/{variationId}',
			'params':           ('productId', 'optionId', 'variationId', ),
			'args':             args
		})

