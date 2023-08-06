# UbiOps Base Connector

This repository contains a template for implementing connectors in UbiOps. It includes basic functionality such as 
mapping data, loading variables and retrying, and provides a structure to implement connectors as UbiOps deployments.

A connector based on this template should import the module and extend the `Connector` class it exposes. For a basic
functional connector only the `insert` method needs to be implemented.

The Connectors repository on the UbiOps Github provides several working connectors that can be used as an example.
