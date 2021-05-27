# Standard library imports

# TODO: Change to make sure that the right type of value is returned using annotations.
class GBDecorators:
    def check_configured(func):
        def modified(self,*args,**kwargs):
            if not self.is_configured():
                raise Exception("Controller not configured")
            return func(self,*args,**kwargs)
        return modified
