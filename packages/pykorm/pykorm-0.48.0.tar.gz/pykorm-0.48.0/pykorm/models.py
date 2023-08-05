import inspect
from typing import Dict

from . import fields
from . import query as pykorm_query


def dict_deep_merge(source: Dict, extra: Dict) -> Dict:
    """
    deep merges two dicts together
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = extra.setdefault(key, {})
            dict_deep_merge(value, node)
        else:
            extra[key] = value

    return extra



class PykormModel:
    name: str = fields.Metadata('name', readonly=True)
    _k8s_uid: str = fields.Metadata('uid', readonly=True)

    _pykorm_group: str
    _pykorm_version: str
    _pykorm_plural: str

    query: pykorm_query.BaseQuery

    @classmethod
    def _get_pykorm_attributes(cls) -> Dict[str, fields.DataField]:
        attributes = inspect.getmembers(cls, lambda a: not(inspect.isroutine(a)))
        obj_attrs = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

        retd = {}
        for obj in obj_attrs:
            (attr_name, attr) = obj
            if isinstance(attr, fields.DataField):
                retd[attr_name] = attr
        return retd

    def __repr__(self):
        repr_dict = {}
        for attr_name in self._get_pykorm_attributes():
            repr_dict[attr_name] = getattr(self, attr_name)

        repr_str = [f'{k}={v}' for k, v in repr_dict.items()]

        return f'<{self.__class__.__name__} {" ".join(repr_str)}>'


    def __setattr__(self, item: str, value):
        pk_attrs = self._get_pykorm_attributes()

        if item in pk_attrs:
            attr = pk_attrs[item]
            now_value = getattr(self, item)

            if now_value is None:
                # Value not previously set, we can set it once (ex: model.name)
                pass
            elif attr.readonly and not isinstance(now_value, fields.DataField):
                # We allow to set the attribute if it was not set before
                raise Exception(f'{item} attribute is read_only !')

        self.__dict__[item] = value


    def __getattribute__(self, item: str):
        attr = object.__getattribute__(self, item)

        if isinstance(attr, fields.DataField):
            return attr.default
        else:
            return attr

    def _matches_attributes(self, filters_dict: Dict[str, str]) -> bool:
        for attribute_name, attribute_value in filters_dict.items():
            if getattr(self, attribute_name) != attribute_value:
                return False
        return True


    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self._k8s_dict == other._k8s_dict


    @classmethod
    def _instantiate_with_dict(cls, k8s_dict) -> 'PykormModel':
        ''' Creates the model with data from the k8s data structure '''
        obj = cls.__new__(cls)
        obj._set_attributes_with_dict(k8s_dict)
        return obj

    def _set_attributes_with_dict(self, k8s_dict: Dict):
        self.__k8s_data = k8s_dict

        for (attr_name, attr_value) in self._get_pykorm_attributes().items():
            value = attr_value.get_data(k8s_dict)
            self.__dict__[attr_name] = value


    @property
    def _k8s_dict(self):
        '''
        Returns the model as a kubernetes dict/yaml structure. This function
        does NOT return readonly fields
        '''
        d = {
            "apiVersion": f'{self._pykorm_group}/{self._pykorm_version}',
            "kind": self.__class__.__name__,
            "metadata": {
                "name": self.name,
            },
            "spec": {
            }
        }

        for (attr_name, attr_type) in self._get_pykorm_attributes().items():
            attr_value = getattr(self, attr_name)

            if attr_type.readonly:
                continue
            elif isinstance(attr_value, fields.DataField):
                attr_value = attr_type.default
            else:
                attr_dict_path = attr_type.to_dict(attr_value)
                d = dict_deep_merge(d, attr_dict_path)
        return d


class NamespacedModel(PykormModel):
    namespace = fields.Metadata('namespace')


class ClusterModel(PykormModel):
    pass

