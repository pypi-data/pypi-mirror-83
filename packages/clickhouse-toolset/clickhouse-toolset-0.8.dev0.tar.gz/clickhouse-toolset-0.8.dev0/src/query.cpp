#include <exception>
#include <iostream>
#include <map>
#include <set>

#include <Python.h>

#include "ClickHouseQuery.h"


static std::string PyObject_AsString(PyObject * obj)
{
    PyObject* o = PyObject_Str(obj);
    PyObject * str = PyUnicode_AsEncodedString(o, "utf-8", "~");
    std::string s = PyBytes_AsString(str);
    Py_DECREF(str);
    Py_DECREF(o);
    return s;
}


static PyObject * format(PyObject * self, PyObject * args)
{
    char * query;

    if (!PyArg_ParseTuple(args, "s", &query))
        return NULL;

    try
    {
        auto formattedQuery = ClickHouseQuery::format(query);
        return Py_BuildValue("s", formattedQuery.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * replaceTables(PyObject * self, PyObject * args, PyObject *keywds)
{
    char * query;
    PyObject * replacementsDict;
    char const * default_database = "";
    static const char* kwlist[] = {"query", "replacements", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "sO!|s", const_cast<char **>(kwlist), &query, &PyDict_Type, &replacementsDict, &default_database))
        return NULL;

    std::map<std::pair<std::string, std::string>, std::pair<std::string, std::string>> replacements;
    PyObject * key, * value;
    Py_ssize_t pos = 0;

    while (PyDict_Next(replacementsDict, &pos, &key, &value)) {
        if (!PyTuple_Check(key))
        {
            PyErr_SetString(PyExc_ValueError, "Key replacement must be a tuple");
            return NULL;
        }
        if (PyTuple_Size(key) != 2)
        {
            PyErr_SetString(PyExc_ValueError, "Key replacement tuple must contain 2 elements");
            return NULL;
        }
        if (!PyTuple_Check(value))
        {
            PyErr_SetString(PyExc_ValueError, "Value replacement must be a tuple");
            return NULL;
        }
        if (PyTuple_Size(value) != 2)
        {
            PyErr_SetString(PyExc_ValueError, "Value replacement tuple must contain 2 elements");
            return NULL;
        }
        replacements.emplace(
            std::make_pair(PyObject_AsString(PyTuple_GetItem(key, 0)), PyObject_AsString(PyTuple_GetItem(key, 1))),
            std::make_pair(PyObject_AsString(PyTuple_GetItem(value, 0)), PyObject_AsString(PyTuple_GetItem(value, 1)))
        );
    }

    try
    {
        auto rewrittenQuery = ClickHouseQuery::replaceTables(default_database, query, replacements);
        return Py_BuildValue("s", rewrittenQuery.data());
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }

}

static PyObject * tables(PyObject * self, PyObject * args, PyObject *keywds)
{
    char * query;
    char const * default_database = "";
    static const char* kwlist[] = {"query", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|s", const_cast<char **>(kwlist), &query, &default_database))
        return NULL;

    try
    {
        auto tablesInQuery = ClickHouseQuery::tables(default_database, query);
        PyObject * l = PyList_New(tablesInQuery.size());
        int i = 0;
        for (const auto table : tablesInQuery)
        {
            PyObject* o = Py_BuildValue("(ss)", table.first.data(), table.second.data());
            PyList_SetItem(l, i++, o);
        }
        return l;
    }
    catch (std::exception & e)
    {
        PyErr_SetString(PyExc_ValueError, e.what());
        return NULL;
    }
}

static PyObject * tableIfIsSimpleQuery(PyObject * self, PyObject * args, PyObject *keywds)
{
    char * query;
    char const * default_database = "";
    static const char* kwlist[] = {"query", "default_database", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywds, "s|s", const_cast<char **>(kwlist), &query, &default_database))
        return NULL;

    try
    {
        if (auto table = ClickHouseQuery::tableIfIsSimpleQuery(default_database, query))
        {
            return Py_BuildValue("(ss)", table->first.data(), table->second.data());
        }
        return Py_BuildValue("");
    }
    catch (std::exception & e)
    {
        return Py_BuildValue("");
    }
}


static PyMethodDef CHToolsetQueryMethods[] =
{
    {"format", format, METH_VARARGS},
    {"_replace_tables", (PyCFunction)replaceTables, METH_VARARGS | METH_KEYWORDS},
    {"tables", (PyCFunction)tables, METH_VARARGS | METH_KEYWORDS},
    {"table_if_is_simple_query", (PyCFunction)tableIfIsSimpleQuery, METH_VARARGS | METH_KEYWORDS},

    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef chquerymodule = {
    PyModuleDef_HEAD_INIT,
    "chtoolset._query",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    CHToolsetQueryMethods
};

PyMODINIT_FUNC
PyInit__query(void)
{
    return PyModule_Create(&chquerymodule);
}
