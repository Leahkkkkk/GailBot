# Standard library imports

# TODO: Change to make sure that the right type of value is returned using annotations.
class OrganizerDecorators:
    def check_configured(func):
        def modified(self,*args,**kwargs):
            if not self.is_configured():
                return lambda self, *args, **kwargs: False
            return func(self,*args,**kwargs)
        return modified