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

// %typemap(in,numinputs=0) MSXproject* (MSXproject temp) {
//     $1 = &temp;
// }

// %typemap(argout) MSXproject* {
//   %append_output(SWIG_NewPointerObj(*$1, SWIGTYPE_p_Project, SWIG_POINTER_NEW));
// }

/* TYPEMAP FOR IGNORING INT ERROR CODE RETURN VALUE */
%typemap(out) int {
    $result = Py_None;
    Py_INCREF($result);
}

%apply int *OUTPUT {
    int *index,
    int *len,
    int *count,
    int *type,
    int *pat
}

%apply double *OUTPUT {
    double *aTol,
    double *rTol,
    double *value,
    double *level
}

%cstring_bounded_output(char *OUTCHAR, MAXMSG);

%apply char *OUTCHAR {
    char *result,
    char *units
}

%apply long *INOUT {
    long *t,
    long *tleft
};

// %nodefault Project;
// struct Project {};
// %extend Project {
//   ~Project() {
//     MSXclose($self);
//   }
// };
// ignore Project;

/* INSERTS CUSTOM EXCEPTION HANDLING IN WRAPPER */
%exception
{
    $action
    if ( result > 10) {
        char errmsg[MAXMSG];
        MSXgeterror(result, errmsg, MAXMSG);
        PyErr_SetString(PyExc_Exception, errmsg);
        SWIG_fail;
    }
    else if (result > 0) {
        PyErr_WarnEx(PyExc_Warning, "WARNING", 2);
    }
}

%feature("autodoc", "2");
// %newobject MSXopen;
// %delobject MSXclose;
%include "msxtoolkit.h"
%include "msxenums.h"
%exception;