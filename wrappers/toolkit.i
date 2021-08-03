/* toolkit.i */

%include "typemaps.i"
%include "cstring.i"
%include "carrays.i"

/* arrays for toolkit functions wanting lists */
%array_class(int, intArray);
%array_class(float, floatArray);

%module (package="epanetmsx") toolkit
%{
/* Put header files here or function declarations like below */
#include "msxtoolkit.h"
%}

/* strip the pseudo-scope from function declarations and enums*/
%rename("%(strip:[MSX])s") "";

/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}

%apply long *INOUT {
    long *t,
    long *tleft
};


/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    $action
    if ( result > 10) {
        char errmsg[ERR_MAX];
        MSXgeterror(result, errmsg, ERR_MAX);
        PyErr_SetString(PyExc_Exception, errmsg);
        SWIG_fail;
    }
    else if (result > 0) {
        PyErr_WarnEx(PyExc_Warning, "WARNING", 2);
    }
}

%feature("autodoc", "2");
%include "msxtoolkit.h"
%exception;