# ----------------------------------------------------------------
def validate(func, locals):
    '''
    - Description: this function validates parameter types for a specific function. 
    '''
    for var, test in func.__annotations__.items():
        if var == "return":
            continue
        value = locals[var]
        msg = f"Error in {func}: {var} argument must be {test}"
        assert isinstance(value,test),msg