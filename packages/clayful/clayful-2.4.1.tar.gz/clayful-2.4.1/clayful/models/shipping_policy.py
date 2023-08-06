class ShippingPolicy:

	Clayful = None
	name = 'ShippingPolicy'
	path = 'shipping/policies'

	@staticmethod
	def config(clayful):

		ShippingPolicy.Clayful = clayful

		return ShippingPolicy

	@staticmethod
	def list(*args):

		return ShippingPolicy.Clayful.call_api({
			'model_name':       ShippingPolicy.name,
			'method_name':      'list',
			'http_method':      'GET',
			'path':             '/v1/shipping/policies',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def count(*args):

		return ShippingPolicy.Clayful.call_api({
			'model_name':       ShippingPolicy.name,
			'method_name':      'count',
			'http_method':      'GET',
			'path':             '/v1/shipping/policies/count',
			'params':           (),
			'args':             args
		})

	@staticmethod
	def get(*args):

		return ShippingPolicy.Clayful.call_api({
			'model_name':       ShippingPolicy.name,
			'method_name':      'get',
			'http_method':      'GET',
			'path':             '/v1/shipping/policies/{shippingPolicyId}',
			'params':           ('shippingPolicyId', ),
			'args':             args
		})

