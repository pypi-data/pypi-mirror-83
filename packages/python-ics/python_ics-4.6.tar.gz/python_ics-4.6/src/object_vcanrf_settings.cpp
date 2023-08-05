#include "object_vcanrf_settings.h"

PyTypeObject vcanrf_settings_object_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    MODULE_NAME "." VCANRF_SETTINGS_OBJECT_NAME, /* tp_name */
    sizeof(vcanrf_settings_object), /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)0,             /* tp_dealloc */
    0,                         /* tp_print */
    (getattrfunc)PyObject_GenericGetAttr, /* tp_getattr */
    (setattrfunc)PyObject_GenericSetAttr, /* tp_setattr */
    0,                         /* tp_reserved */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */ 
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    PyObject_GenericGetAttr,   /* tp_getattro */
    PyObject_GenericSetAttr,   /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
    Py_TPFLAGS_BASETYPE,       /* tp_flags */
    VCANRF_SETTINGS_OBJECT_NAME" object",      /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    0,                         /* tp_methods */
    vcanrf_settings_object_members, /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)vcanrf_settings_object_init, /* tp_init */
    0,                         /* tp_alloc */
    0,                         /* tp_new */
};

bool setup_vcanrf_settings_object(PyObject* module)
{
    vcanrf_settings_object_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&vcanrf_settings_object_type) < 0) {
        return false;
    }
    Py_INCREF(&vcanrf_settings_object_type);
    PyModule_AddObject(module, VCANRF_SETTINGS_OBJECT_NAME, (PyObject*)&vcanrf_settings_object_type);
    return true;
}
