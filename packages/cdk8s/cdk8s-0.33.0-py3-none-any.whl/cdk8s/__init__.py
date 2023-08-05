"""
# cdk8s

> Cloud Development Kit for Kubernetes

**cdk8s** is a software development framework for defining Kubernetes
applications using rich object-oriented APIs. It allows developers to leverage
the full power of software in order to define abstract components called
"constructs" which compose Kubernetes resources or other constructs into
higher-level abstractions.

This library is the foundation of **cdk8s**. It includes base types that are
used to define cdk8s applications.

## Chart

The `Chart` is a container that synthesizes a single Kubernetes manifest.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class MyChart(Chart):
    def __init__(self, scope, ns):
        super().__init__(scope, ns)
```

During synthesis, charts collect all the `ApiObject` nodes (recursively) and
emit a single YAML manifest that includes all these objects.

When a chart is defined, you can specify chart-level `namespace` and `labels`.
Those will be applied to all API objects defined within the chart (recursively):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class MyChart(Chart):
    def __init__(self, scope, ns):
        super().__init__(scope, ns,
            namespace="my-namespace",
            labels={
                "app": "my-app"
            }
        )

        ApiObject(self, "my-object",
            api_version="v1",
            kind="Foo"
        )
```

Will synthesize into:

```yaml
apiVersion: v1
kind: Foo
metadata:
  namesapce: my-namespace
  labels:
    app: my-app
```

## ApiObject

An `ApiObject` is a construct that represents an entry in a Kubernetes manifest (level 0).
In most cases, you won't use `ApiObject` directly but rather use classes that
are imported through `cdk8s import` and which extend this base class.

## Include

The `Include` construct can be used to include an existing manifest in a chart.

The following example will include the Kubernetes Dashboard in `MyChart`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import Include

class MyChart(Chart):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        dashboard = Include(self, "dashboard", {
            "url": "https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml",
            # or
            "url": "dashboard.yaml"
        })
```

All API objects defined in the included manifest will be added as children
`ApiObject`s under the `Include` construct's scope and can be accessed
through the `apiObject` property:

The following example queries for all the `Deployment` resources in the
dashboard:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_api_object = dashboard.api_objects.find(c => c.kind === 'Deployment);)
```

NOTE: names of included objects (`metadata.name`) are preserved. This means that
if you try to include the same manifest twice into the same chart, your manifest
will have duplicate definitions of the same objects.

## Dependencies

You can declare dependencies between any two cdk8s constructs using the `addDependency()` method.

### ApiObjects

For example, you can force kubernetes to first apply a `Namespace` before applying the `Service` in the scope of that namespace:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
namespace = k8s.Namespace(chart, "backend")
service = k8s.Service(chart, "Service", metadata={"namespace": namespace.name})

# declare the dependency. this is just a syntactic sugar for Node.of(service).addDependency(namespace)
service.add_dependency(namespace)
```

`cdk8s` will ensure that the `Namespace` object is placed before the `Service` object in the resulting manifest:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: chart-backend-a59d2e47
---
apiVersion: v1
kind: Service
metadata:
  name: chart-service-93d02be7
  namespace: chart-backend-a59d2e47
```

### Charts

You can also specify dependencies between charts, in exactly the same manner. For example, if we have a chart that provisions our `namespace`, we need that chart to be applied first:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
namespace_chart = NamespaceChart(app, "namespace")
application_chart = ApplicationChart(app, "application")

# declare the dependency. this is just a syntactic sugar for Node.of(applicationChart).addDependency(namespaceChart)
application_chart.add_dependency(namespace_chart)
```

Running `cdk8s synth` will produce the following `dist` directory:

```console
> cdk8s synth

dist/0000-namespace.k8s.yaml
dist/0001-application.k8s.yaml
```

Notice that the `namespace` chart appears first with the `0000` prefix. This will ensure that a subsequent execution of `kubectl apply -f dist/` will apply the `namespace` first, and the `application` second.

### Custom Constructs

The behavior above applies in the same way to custom constructs that you create or use.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class Database(Construct):
    def __init__(self, scope, name):
        super().__init__(scope, name)

        k8s.StatefulSet(self, "StatefulSet")
        k8s.ConfigMap(self, "ConfigMap")

app = App()

chart = Chart(app, "Chart")

service = k8s.Service(chart, "Service")
database = Database(chart, "Database")

service.add_dependency(database)
```

Declaring such a dependency will cause **each** `ApiObject` in the source construct, to *depend on* **every** `ApiObject` in the target construct.

Note that in the example above, the source construct is actually an `ApiObject`, which is also ok since it is essentially a construct with a single `ApiObject`.

> Note that if the source of your dependency is a custom construct, it won't have the `addDependency` syntactic sugar by default, so you'll have to use `Node.of()`.

The resulting manifest will be:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: chart-database-statefulset-4627f8e2
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: chart-database-configmap-676f8640
---
apiVersion: v1
kind: Service
metadata:
  name: chart-service-93d02be7
```

You can see that all `ApiObject`s of the `Database` construct, appear before the `Service` object.

### Things just got cool

If you simply declare a dependency between two `ApiObject`s (or `Constructs`), that belong to two different `Chart`s, `cdk8s` will create the chart dependency automatically for you.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
namespace_chart = NamespaceChart(app, "namespace")
application_chart = ApplicationChart(app, "application")

namespace = k8s.Namespace(namespace_chart, "namespace")
deployment = k8s.Deployment(application_chart, "Deployment")

# dependency between ApiObjects, not Charts!
deployment.add_dependency(namespace)
```

Running `cdk8s synth` will produce the same result as if explicit chart dependencies were declared:

```console
> cdk8s synth

dist/0000-namespace.k8s.yaml
dist/0001-application.k8s.yaml
```

This means you need not be bothered with managing chart dependencies, simply work with the `ApiObject`s you create, and let `cdk8s` infer the chart dependencies.

## Helm Support

You can use the `Helm` construct in order to include [Helm](https://helm.sh)
charts.

In order to use this construct, you must have `helm` installed on your system.
See [Installing Helm](https://helm.sh/docs/intro/install/) in the Helm
documentation for details.

The following example adds the
[bitnami/redis](https://github.com/bitnami/charts/tree/master/bitnami/redis)
Helm chart with sentinel containers enabled:

> The Bitnami helm repo needs to be added through: `helm repo add bitnami https://charts.bitnami.com/bitnami`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
class MyChart(cdk8s.Chart):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        redis = Helm(self, "redis",
            chart="bitnami/redis",
            values={
                "sentinel": {
                    "enabled": True
                }
            }
        )
```

The `Helm` construct will render the manifest from the specified chart by
executing `helm template`. If `values` is specified, these values will override
the default values included with the chart.

The `name` option can be used to specify the chart's [release name](https://helm.sh/docs/intro/using_helm/#three-big-concepts).
If not specified, a valid and unique release name will be allocated
based on the construct path.

The `Helm` construct extends `Include` and inherits it's API. For example, you
can use the `apiObjects` property to find and interact with included API
objects.

The following example shows how to add an annotation to the Redis master
deployment:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
master = redis.api_objects.find(o => o.name === 'foo-redis-master);,
    master.metadata.add_annotation("my.annotation", "hey-there"))
```

## Testing

cdk8s bundles a set of test utilities under the `Testing` class:

* `Testing.app()` returns an `App` object bound to a temporary output directory.
* `Testing.chart()` returns a `Chart` object bound to a testing app.
* `Testing.synth(chart)` returns the Kubernetes manifest synthesized from a
  chart.

## License

This project is distributed under the [Apache License, Version 2.0](./LICENSE).

This module is part of the [cdk8s project](https://github.com/awslabs/cdk8s).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import constructs


class ApiObject(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.ApiObject",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        ns: builtins.str,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        metadata: typing.Optional["ApiObjectMetadata"] = None,
    ) -> None:
        """(experimental) Defines an API object.

        :param scope: the construct scope.
        :param ns: namespace.
        :param api_version: (experimental) API version.
        :param kind: (experimental) Resource kind.
        :param metadata: (experimental) Object metadata. If ``name`` is not specified, an app-unique name will be allocated by the framework based on the path of the construct within thes construct tree.

        :stability: experimental
        """
        options = ApiObjectOptions(
            api_version=api_version, kind=kind, metadata=metadata
        )

        jsii.create(ApiObject, self, [scope, ns, options])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: constructs.IConstruct) -> None:
        """(experimental) Create a dependency between this ApiObject and other constructs.

        These can be other ApiObjects, Charts, or custom.

        :param dependencies: the dependencies to add.

        :stability: experimental
        """
        return jsii.invoke(self, "addDependency", [*dependencies])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        """(experimental) Renders the object to Kubernetes JSON.

        :stability: experimental
        """
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiGroup")
    def api_group(self) -> builtins.str:
        """(experimental) The group portion of the API version (e.g. ``authorization.k8s.io``).

        :stability: experimental
        """
        return jsii.get(self, "apiGroup")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiVersion")
    def api_version(self) -> builtins.str:
        """(experimental) The object's API version (e.g. ``authorization.k8s.io/v1``).

        :stability: experimental
        """
        return jsii.get(self, "apiVersion")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="chart")
    def chart(self) -> "Chart":
        """(experimental) The chart in which this object is defined.

        :stability: experimental
        """
        return jsii.get(self, "chart")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        """(experimental) The object kind.

        :stability: experimental
        """
        return jsii.get(self, "kind")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "ApiObjectMetadataDefinition":
        """(experimental) Metadata associated with this API object.

        :stability: experimental
        """
        return jsii.get(self, "metadata")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """(experimental) The name of the API object.

        If a name is specified in ``metadata.name`` this will be the name returned.
        Otherwise, a name will be generated by calling
        ``Chart.of(this).generatedObjectName(this)``, which by default uses the
        construct path to generate a DNS-compatible name for the resource.

        :stability: experimental
        """
        return jsii.get(self, "name")


@jsii.data_type(
    jsii_type="cdk8s.ApiObjectMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "labels": "labels",
        "name": "name",
        "namespace": "namespace",
    },
)
class ApiObjectMetadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Metadata associated with this object.

        :param annotations: (experimental) Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. Default: - No annotations.
        :param labels: (experimental) Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. Default: - No labels.
        :param name: (experimental) The unique, namespace-global, name of this object inside the Kubernetes cluster. Normally, you shouldn't specify names for objects and let the CDK generate a name for you that is application-unique. The names CDK generates are composed from the construct path components, separated by dots and a suffix that is based on a hash of the entire path, to ensure uniqueness. You can supply custom name allocation logic by overriding the ``chart.generateObjectName`` method. If you use an explicit name here, bear in mind that this reduces the composability of your construct because it won't be possible to include more than one instance in any app. Therefore it is highly recommended to leave this unspecified. Default: - an app-unique name generated by the chart
        :param namespace: (experimental) Namespace defines the space within each name must be unique. An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces Default: undefined (will be assigned to the 'default' namespace)

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata.

        They are not queryable and should be
        preserved when modifying objects.

        :default: - No annotations.

        :see: http://kubernetes.io/docs/user-guide/annotations
        :stability: experimental
        """
        result = self._values.get("annotations")
        return result

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Map of string keys and values that can be used to organize and categorize (scope and select) objects.

        May match selectors of replication controllers and services.

        :default: - No labels.

        :see: http://kubernetes.io/docs/user-guide/labels
        :stability: experimental
        """
        result = self._values.get("labels")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """(experimental) The unique, namespace-global, name of this object inside the Kubernetes cluster.

        Normally, you shouldn't specify names for objects and let the CDK generate
        a name for you that is application-unique. The names CDK generates are
        composed from the construct path components, separated by dots and a suffix
        that is based on a hash of the entire path, to ensure uniqueness.

        You can supply custom name allocation logic by overriding the
        ``chart.generateObjectName`` method.

        If you use an explicit name here, bear in mind that this reduces the
        composability of your construct because it won't be possible to include
        more than one instance in any app. Therefore it is highly recommended to
        leave this unspecified.

        :default: - an app-unique name generated by the chart

        :stability: experimental
        """
        result = self._values.get("name")
        return result

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        """(experimental) Namespace defines the space within each name must be unique.

        An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation.
        Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces

        :default: undefined (will be assigned to the 'default' namespace)

        :stability: experimental
        """
        result = self._values.get("namespace")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiObjectMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiObjectMetadataDefinition(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s.ApiObjectMetadataDefinition",
):
    """(experimental) Object metadata.

    :stability: experimental
    """

    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param annotations: (experimental) Annotations is an unstructured key value map stored with a resource that may be set by external tools to store and retrieve arbitrary metadata. They are not queryable and should be preserved when modifying objects. Default: - No annotations.
        :param labels: (experimental) Map of string keys and values that can be used to organize and categorize (scope and select) objects. May match selectors of replication controllers and services. Default: - No labels.
        :param name: (experimental) The unique, namespace-global, name of this object inside the Kubernetes cluster. Normally, you shouldn't specify names for objects and let the CDK generate a name for you that is application-unique. The names CDK generates are composed from the construct path components, separated by dots and a suffix that is based on a hash of the entire path, to ensure uniqueness. You can supply custom name allocation logic by overriding the ``chart.generateObjectName`` method. If you use an explicit name here, bear in mind that this reduces the composability of your construct because it won't be possible to include more than one instance in any app. Therefore it is highly recommended to leave this unspecified. Default: - an app-unique name generated by the chart
        :param namespace: (experimental) Namespace defines the space within each name must be unique. An empty namespace is equivalent to the "default" namespace, but "default" is the canonical representation. Not all objects are required to be scoped to a namespace - the value of this field for those objects will be empty. Must be a DNS_LABEL. Cannot be updated. More info: http://kubernetes.io/docs/user-guide/namespaces Default: undefined (will be assigned to the 'default' namespace)

        :stability: experimental
        """
        options = ApiObjectMetadata(
            annotations=annotations, labels=labels, name=name, namespace=namespace
        )

        jsii.create(ApiObjectMetadataDefinition, self, [options])

    @jsii.member(jsii_name="add")
    def add(self, key: builtins.str, value: typing.Any) -> None:
        """(experimental) Adds an arbitrary key/value to the object metadata.

        :param key: Metadata key.
        :param value: Metadata value.

        :stability: experimental
        """
        return jsii.invoke(self, "add", [key, value])

    @jsii.member(jsii_name="addAnnotation")
    def add_annotation(self, key: builtins.str, value: builtins.str) -> None:
        """(experimental) Add an annotation.

        :param key: - The key.
        :param value: - The value.

        :stability: experimental
        """
        return jsii.invoke(self, "addAnnotation", [key, value])

    @jsii.member(jsii_name="addLabel")
    def add_label(self, key: builtins.str, value: builtins.str) -> None:
        """(experimental) Add a label.

        :param key: - The key.
        :param value: - The value.

        :stability: experimental
        """
        return jsii.invoke(self, "addLabel", [key, value])

    @jsii.member(jsii_name="getLabel")
    def get_label(self, key: builtins.str) -> typing.Optional[builtins.str]:
        """
        :param key: the label.

        :return: a value of a label or undefined

        :stability: experimental
        """
        return jsii.invoke(self, "getLabel", [key])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.Any:
        """(experimental) Synthesizes a k8s ObjectMeta for this metadata set.

        :stability: experimental
        """
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the API object.

        If a name is specified in ``metadata.name`` this will be the name returned.
        Otherwise, a name will be generated by calling
        ``Chart.of(this).generatedObjectName(this)``, which by default uses the
        construct path to generate a DNS-compatible name for the resource.

        :stability: experimental
        """
        return jsii.get(self, "name")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        """(experimental) The object's namespace.

        :stability: experimental
        """
        return jsii.get(self, "namespace")


@jsii.data_type(
    jsii_type="cdk8s.ApiObjectOptions",
    jsii_struct_bases=[],
    name_mapping={"api_version": "apiVersion", "kind": "kind", "metadata": "metadata"},
)
class ApiObjectOptions:
    def __init__(
        self,
        *,
        api_version: builtins.str,
        kind: builtins.str,
        metadata: typing.Optional[ApiObjectMetadata] = None,
    ) -> None:
        """(experimental) Options for defining API objects.

        :param api_version: (experimental) API version.
        :param kind: (experimental) Resource kind.
        :param metadata: (experimental) Object metadata. If ``name`` is not specified, an app-unique name will be allocated by the framework based on the path of the construct within thes construct tree.

        :stability: experimental
        """
        if isinstance(metadata, dict):
            metadata = ApiObjectMetadata(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "api_version": api_version,
            "kind": kind,
        }
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def api_version(self) -> builtins.str:
        """(experimental) API version.

        :stability: experimental
        """
        result = self._values.get("api_version")
        assert result is not None, "Required property 'api_version' is missing"
        return result

    @builtins.property
    def kind(self) -> builtins.str:
        """(experimental) Resource kind.

        :stability: experimental
        """
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return result

    @builtins.property
    def metadata(self) -> typing.Optional[ApiObjectMetadata]:
        """(experimental) Object metadata.

        If ``name`` is not specified, an app-unique name will be allocated by the
        framework based on the path of the construct within thes construct tree.

        :stability: experimental
        """
        result = self._values.get("metadata")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiObjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s.App"):
    """(experimental) Represents a cdk8s application.

    :stability: experimental
    """

    def __init__(self, *, outdir: typing.Optional[builtins.str] = None) -> None:
        """(experimental) Defines an app.

        :param outdir: (experimental) The directory to output Kubernetes manifests. Default: - CDK8S_OUTDIR if defined, otherwise "dist"

        :stability: experimental
        """
        options = AppOptions(outdir=outdir)

        jsii.create(App, self, [options])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        """(experimental) Synthesizes all manifests to the output directory.

        :stability: experimental
        """
        return jsii.invoke(self, "synth", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        """(experimental) The output directory into which manifests will be synthesized.

        :stability: experimental
        """
        return jsii.get(self, "outdir")


@jsii.data_type(
    jsii_type="cdk8s.AppOptions",
    jsii_struct_bases=[],
    name_mapping={"outdir": "outdir"},
)
class AppOptions:
    def __init__(self, *, outdir: typing.Optional[builtins.str] = None) -> None:
        """
        :param outdir: (experimental) The directory to output Kubernetes manifests. Default: - CDK8S_OUTDIR if defined, otherwise "dist"

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if outdir is not None:
            self._values["outdir"] = outdir

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        """(experimental) The directory to output Kubernetes manifests.

        :default: - CDK8S_OUTDIR if defined, otherwise "dist"

        :stability: experimental
        """
        result = self._values.get("outdir")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Chart(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Chart"):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        ns: builtins.str,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param ns: -
        :param labels: (experimental) Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: (experimental) The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")

        :stability: experimental
        """
        options = ChartOptions(labels=labels, namespace=namespace)

        jsii.create(Chart, self, [scope, ns, options])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, c: constructs.IConstruct) -> "Chart":
        """(experimental) Finds the chart in which a node is defined.

        :param c: a construct node.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [c])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *dependencies: constructs.IConstruct) -> None:
        """(experimental) Create a dependency between this Chart and other constructs.

        These can be other ApiObjects, Charts, or custom.

        :param dependencies: the dependencies to add.

        :stability: experimental
        """
        return jsii.invoke(self, "addDependency", [*dependencies])

    @jsii.member(jsii_name="generateObjectName")
    def generate_object_name(self, api_object: ApiObject) -> builtins.str:
        """(experimental) Generates a app-unique name for an object given it's construct node path.

        Different resource types may have different constraints on names
        (``metadata.name``). The previous version of the name generator was
        compatible with DNS_SUBDOMAIN but not with DNS_LABEL.

        For example, ``Deployment`` names must comply with DNS_SUBDOMAIN while
        ``Service`` names must comply with DNS_LABEL.

        Since there is no formal specification for this, the default name
        generation scheme for kubernetes objects in cdk8s was changed to DNS_LABEL,
        since it’s the common denominator for all kubernetes resources
        (supposedly).

        You can override this method if you wish to customize object names at the
        chart level.

        :param api_object: The API object to generate a name for.

        :stability: experimental
        """
        return jsii.invoke(self, "generateObjectName", [api_object])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """(experimental) Renders this chart to a set of Kubernetes JSON resources.

        :return: array of resource manifests

        :stability: experimental
        """
        return jsii.invoke(self, "toJson", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        """(experimental) Labels applied to all resources in this chart.

        This is an immutable copy.

        :stability: experimental
        """
        return jsii.get(self, "labels")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> typing.Optional[builtins.str]:
        """(experimental) The default namespace for all objects in this chart.

        :stability: experimental
        """
        return jsii.get(self, "namespace")


@jsii.data_type(
    jsii_type="cdk8s.ChartOptions",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "namespace": "namespace"},
)
class ChartOptions:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param labels: (experimental) Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: (experimental) The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Labels to apply to all resources in this chart.

        :default: - no common labels

        :stability: experimental
        """
        result = self._values.get("labels")
        return result

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        """(experimental) The default namespace for all objects defined in this chart (directly or indirectly).

        This namespace will only apply to objects that don't have a
        ``namespace`` explicitly defined for them.

        :default: - no namespace is synthesized (usually this implies "default")

        :stability: experimental
        """
        result = self._values.get("namespace")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChartOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DependencyGraph(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.DependencyGraph"):
    """(experimental) Represents the dependency graph for a given Node.

    This graph includes the dependency relationships between all nodes in the
    node (construct) sub-tree who's root is this Node.

    Note that this means that lonely nodes (no dependencies and no dependants) are also included in this graph as
    childless children of the root node of the graph.

    The graph does not include cross-scope dependencies. That is, if a child on the current scope depends on a node
    from a different scope, that relationship is not represented in this graph.

    :stability: experimental
    """

    def __init__(self, node: constructs.Node) -> None:
        """
        :param node: -

        :stability: experimental
        """
        jsii.create(DependencyGraph, self, [node])

    @jsii.member(jsii_name="topology")
    def topology(self) -> typing.List[constructs.IConstruct]:
        """
        :see: Vertex.topology()
        :stability: experimental
        """
        return jsii.invoke(self, "topology", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="root")
    def root(self) -> "DependencyVertex":
        """(experimental) Returns the root of the graph.

        Note that this vertex will always have ``null`` as its ``.value`` since it is an artifical root
        that binds all the connected spaces of the graph.

        :stability: experimental
        """
        return jsii.get(self, "root")


class DependencyVertex(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.DependencyVertex"):
    """(experimental) Represents a vertex in the graph.

    The value of each vertex is an ``IConstruct`` that is accessible via the ``.value`` getter.

    :stability: experimental
    """

    def __init__(self, value: typing.Optional[constructs.IConstruct] = None) -> None:
        """
        :param value: -

        :stability: experimental
        """
        jsii.create(DependencyVertex, self, [value])

    @jsii.member(jsii_name="addChild")
    def add_child(self, dep: "DependencyVertex") -> None:
        """(experimental) Adds a vertex as a dependency of the current node.

        Also updates the parents of ``dep``, so that it contains this node as a parent.

        This operation will fail in case it creates a cycle in the graph.

        :param dep: The dependency.

        :stability: experimental
        """
        return jsii.invoke(self, "addChild", [dep])

    @jsii.member(jsii_name="topology")
    def topology(self) -> typing.List[constructs.IConstruct]:
        """(experimental) Returns a topologically sorted array of the constructs in the sub-graph.

        :stability: experimental
        """
        return jsii.invoke(self, "topology", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="inbound")
    def inbound(self) -> typing.List["DependencyVertex"]:
        """(experimental) Returns the parents of the vertex (i.e dependants).

        :stability: experimental
        """
        return jsii.get(self, "inbound")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outbound")
    def outbound(self) -> typing.List["DependencyVertex"]:
        """(experimental) Returns the children of the vertex (i.e dependencies).

        :stability: experimental
        """
        return jsii.get(self, "outbound")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Optional[constructs.IConstruct]:
        """(experimental) Returns the IConstruct this graph vertex represents.

        ``null`` in case this is the root of the graph.

        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(
    jsii_type="cdk8s.HelmOptions",
    jsii_struct_bases=[],
    name_mapping={
        "chart": "chart",
        "helm_executable": "helmExecutable",
        "helm_flags": "helmFlags",
        "release_name": "releaseName",
        "values": "values",
    },
)
class HelmOptions:
    def __init__(
        self,
        *,
        chart: builtins.str,
        helm_executable: typing.Optional[builtins.str] = None,
        helm_flags: typing.Optional[typing.List[builtins.str]] = None,
        release_name: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """(experimental) Options for ``Helm``.

        :param chart: (experimental) The chart name to use. It can be a chart from a helm repository or a local directory. This name is passed to ``helm template`` and has all the relevant semantics.
        :param helm_executable: (experimental) The local helm executable to use in order to create the manifest the chart. Default: "helm"
        :param helm_flags: (experimental) Additional flags to add to the ``helm`` execution. Default: []
        :param release_name: (experimental) The release name. Default: - if unspecified, a name will be allocated based on the construct path
        :param values: (experimental) Values to pass to the chart. Default: - If no values are specified, chart will use the defaults.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "chart": chart,
        }
        if helm_executable is not None:
            self._values["helm_executable"] = helm_executable
        if helm_flags is not None:
            self._values["helm_flags"] = helm_flags
        if release_name is not None:
            self._values["release_name"] = release_name
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def chart(self) -> builtins.str:
        """(experimental) The chart name to use. It can be a chart from a helm repository or a local directory.

        This name is passed to ``helm template`` and has all the relevant semantics.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "bitnami/redis"
        """
        result = self._values.get("chart")
        assert result is not None, "Required property 'chart' is missing"
        return result

    @builtins.property
    def helm_executable(self) -> typing.Optional[builtins.str]:
        """(experimental) The local helm executable to use in order to create the manifest the chart.

        :default: "helm"

        :stability: experimental
        """
        result = self._values.get("helm_executable")
        return result

    @builtins.property
    def helm_flags(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) Additional flags to add to the ``helm`` execution.

        :default: []

        :stability: experimental
        """
        result = self._values.get("helm_flags")
        return result

    @builtins.property
    def release_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The release name.

        :default: - if unspecified, a name will be allocated based on the construct path

        :see: https://helm.sh/docs/intro/using_helm/#three-big-concepts
        :stability: experimental
        """
        result = self._values.get("release_name")
        return result

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(experimental) Values to pass to the chart.

        :default: - If no values are specified, chart will use the defaults.

        :stability: experimental
        """
        result = self._values.get("values")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk8s.IAnyProducer")
class IAnyProducer(typing_extensions.Protocol):
    """
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        """
        :stability: experimental
        """
        ...


class _IAnyProducerProxy:
    """
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "cdk8s.IAnyProducer"

    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [])


class Include(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Include"):
    """(experimental) Reads a YAML manifest from a file or a URL and defines all resources as API objects within the defined scope.

    The names (``metadata.name``) of imported resources will be preserved as-is
    from the manifest.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        url: builtins.str,
    ) -> None:
        """
        :param scope: -
        :param name: -
        :param url: (experimental) Local file path or URL which includes a Kubernetes YAML manifest.

        :stability: experimental
        """
        options = IncludeOptions(url=url)

        jsii.create(Include, self, [scope, name, options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="apiObjects")
    def api_objects(self) -> typing.List[ApiObject]:
        """(experimental) Returns all the included API objects.

        :stability: experimental
        """
        return jsii.get(self, "apiObjects")


@jsii.data_type(
    jsii_type="cdk8s.IncludeOptions",
    jsii_struct_bases=[],
    name_mapping={"url": "url"},
)
class IncludeOptions:
    def __init__(self, *, url: builtins.str) -> None:
        """
        :param url: (experimental) Local file path or URL which includes a Kubernetes YAML manifest.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "url": url,
        }

    @builtins.property
    def url(self) -> builtins.str:
        """(experimental) Local file path or URL which includes a Kubernetes YAML manifest.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            mymanifest.yaml
        """
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Lazy"):
    """
    :stability: experimental
    """

    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, producer: IAnyProducer) -> typing.Any:
        """
        :param producer: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "any", [producer])

    @jsii.member(jsii_name="produce")
    def produce(self) -> typing.Any:
        """
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [])


class Names(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Names"):
    """(experimental) Utilities for generating unique and stable names.

    :stability: experimental
    """

    @jsii.member(jsii_name="toDnsLabel")
    @builtins.classmethod
    def to_dns_label(
        cls,
        path: builtins.str,
        max_len: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        """(experimental) Generates a unique and stable name compatible DNS_LABEL from RFC-1123 from a path.

        The generated name will:

        - contain at most 63 characters
        - contain only lowercase alphanumeric characters or ‘-’
        - start with an alphanumeric character
        - end with an alphanumeric character

        The generated name will have the form:
        --..--

        Where  are the path components (assuming they are is separated by
        "/").

        Note that if the total length is longer than 63 characters, we will trim
        the first components since the last components usually encode more meaning.

        :param path: a path to a node (components separated by "/").
        :param max_len: maximum allowed length for name.

        :stability: experimental
        :link: https://tools.ietf.org/html/rfc1123
        :throws:

        if any of the components do not adhere to naming constraints or
        length.
        """
        return jsii.sinvoke(cls, "toDnsLabel", [path, max_len])

    @jsii.member(jsii_name="toLabelValue")
    @builtins.classmethod
    def to_label_value(
        cls,
        path: builtins.str,
        delim: typing.Optional[builtins.str] = None,
        max_len: typing.Optional[jsii.Number] = None,
    ) -> builtins.str:
        """(experimental) Generates a unique and stable name compatible label key name segment and label value from a path.

        The name segment is required and must be 63 characters or less, beginning
        and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-),
        underscores (_), dots (.), and alphanumerics between.

        Valid label values must be 63 characters or less and must be empty or
        begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes
        (-), underscores (_), dots (.), and alphanumerics between.

        The generated name will have the form:
        ..

        Where  are the path components (assuming they are is separated by
        "/").

        Note that if the total length is longer than 63 characters, we will trim
        the first components since the last components usually encode more meaning.

        :param path: a path to a node (components separated by "/").
        :param delim: a delimiter to separates components.
        :param max_len: maximum allowed length for name.

        :stability: experimental
        :link: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
        :throws:

        if any of the components do not adhere to naming constraints or
        length.
        """
        return jsii.sinvoke(cls, "toLabelValue", [path, delim, max_len])


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Testing"):
    """(experimental) Testing utilities for cdk8s applications.

    :stability: experimental
    """

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(cls) -> App:
        """(experimental) Returns an app for testing with the following properties: - Output directory is a temp dir.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "app", [])

    @jsii.member(jsii_name="chart")
    @builtins.classmethod
    def chart(cls) -> Chart:
        """
        :return: a Chart that can be used for tests

        :stability: experimental
        """
        return jsii.sinvoke(cls, "chart", [])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, chart: Chart) -> typing.List[typing.Any]:
        """(experimental) Returns the Kubernetes manifest synthesized from this chart.

        :param chart: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "synth", [chart])


class Yaml(metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Yaml"):
    """(experimental) YAML utilities.

    :stability: experimental
    """

    @jsii.member(jsii_name="load")
    @builtins.classmethod
    def load(cls, url_or_file: builtins.str) -> typing.List[typing.Any]:
        """(experimental) Downloads a set of YAML documents (k8s manifest for example) from a URL or a file and returns them as javascript objects.

        Empty documents are filtered out.

        :param url_or_file: a URL of a file path to load from.

        :return: an array of objects, each represents a document inside the YAML

        :stability: experimental
        """
        return jsii.sinvoke(cls, "load", [url_or_file])

    @jsii.member(jsii_name="save")
    @builtins.classmethod
    def save(cls, file_path: builtins.str, docs: typing.List[typing.Any]) -> None:
        """(experimental) Saves a set of objects as a multi-document YAML file.

        :param file_path: The output path.
        :param docs: The set of objects.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "save", [file_path, docs])

    @jsii.member(jsii_name="tmp")
    @builtins.classmethod
    def tmp(cls, docs: typing.List[typing.Any]) -> builtins.str:
        """(experimental) Saves a set of YAML documents into a temp file (in /tmp).

        :param docs: the set of documents to save.

        :return: the path to the temporary file

        :stability: experimental
        """
        return jsii.sinvoke(cls, "tmp", [docs])


class Helm(Include, metaclass=jsii.JSIIMeta, jsii_type="cdk8s.Helm"):
    """(experimental) Represents a Helm deployment.

    Use this construct to import an existing Helm chart and incorporate it into your constructs.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        chart: builtins.str,
        helm_executable: typing.Optional[builtins.str] = None,
        helm_flags: typing.Optional[typing.List[builtins.str]] = None,
        release_name: typing.Optional[builtins.str] = None,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param chart: (experimental) The chart name to use. It can be a chart from a helm repository or a local directory. This name is passed to ``helm template`` and has all the relevant semantics.
        :param helm_executable: (experimental) The local helm executable to use in order to create the manifest the chart. Default: "helm"
        :param helm_flags: (experimental) Additional flags to add to the ``helm`` execution. Default: []
        :param release_name: (experimental) The release name. Default: - if unspecified, a name will be allocated based on the construct path
        :param values: (experimental) Values to pass to the chart. Default: - If no values are specified, chart will use the defaults.

        :stability: experimental
        """
        opts = HelmOptions(
            chart=chart,
            helm_executable=helm_executable,
            helm_flags=helm_flags,
            release_name=release_name,
            values=values,
        )

        jsii.create(Helm, self, [scope, id, opts])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="releaseName")
    def release_name(self) -> builtins.str:
        """(experimental) The helm release name.

        :stability: experimental
        """
        return jsii.get(self, "releaseName")


__all__ = [
    "ApiObject",
    "ApiObjectMetadata",
    "ApiObjectMetadataDefinition",
    "ApiObjectOptions",
    "App",
    "AppOptions",
    "Chart",
    "ChartOptions",
    "DependencyGraph",
    "DependencyVertex",
    "Helm",
    "HelmOptions",
    "IAnyProducer",
    "Include",
    "IncludeOptions",
    "Lazy",
    "Names",
    "Testing",
    "Yaml",
]

publication.publish()
