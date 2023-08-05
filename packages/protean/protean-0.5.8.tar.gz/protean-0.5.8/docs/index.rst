Protean
=======

Release v\ |version| (:ref:`Changelog <changelog>`)

.. image:: https://travis-ci.org/proteanhq/protean.svg?branch=master
    :target: https://travis-ci.org/proteanhq/protean
    :alt: Build Status
.. image:: https://codecov.io/gh/proteanhq/protean/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/proteanhq/protean
    :alt: Coverage
.. image:: https://pyup.io/repos/github/proteanhq/protean/shield.svg
     :target: https://pyup.io/repos/github/proteanhq/protean/
     :alt: Updates

*The Pragmatic Framework for Ambitious Applications*

Get started with :ref:`install` and follow through with the :ref:`quickstart` guide. The rest of the docs deep-dive into different aspects of Protean.

Overview
--------
**Protean Framework** helps you build applications that can scale and adapt to growing requirements without significant rework.

At its core, Protean encourages a Domain-driven design (DDD) approach to building applications, while providing the tools necessary to express your domain succinctly and precisely. It also allows you to remain agnostic to the underlying technology by keeping implementation details out of view, helping you delay infrastructure decisions until the |last-responsible-moment|.

Protean can be thought of containing three parts:

1. **Service-Oriented**: Protean helps decompose a domain into one or more subdomains, that can run independently as Microservices
2. **Event-Driven**: Protean advocates using Domain Events both to propagate changes across different subdomains as well as to achieve eventual consistency in a Bounded Context.
3. **Adapter-based**: Protean helps you remain technology-agnostic by exposing Port interfaces to the infrastructure, with multiple adapters supported out of the box.

Read :ref:`foreword` and check out the full list of :ref:`key-features` to understand Protean's philosophy.

Protean is an excellent fit for:

- Greenfield projects in complex and uncharted domains, where experimentation and refactoring is a necessity
- Porting complicated Legacy applications onto newer technology stacks
- Building long-term products that need to adapt and evolve over time

Protean helps you develop faster and better, and cleaner code by:
- Providing a toolkit to model the code as closely as possible after the domain
- Allowing you to delay important decisions until the Last Responsible Moment (LRM) and switch later easily if necessary
- Aligning your development team with good practices that result in quality software
- Helping you remain technology-agnostic with the help of a Plugin-based Architecture

*Protean is free, open source, and always will be.*

.. note:: It is assumed that you have some prior knowledge about **Domain-driven Design** and **Command Query Responsibility Segregation** architectural patterns.

    If you do not have sufficient background in these topics, you should go through the following texts:

    * |ddd-eric-evans|
    * |implementing-ddd-vaughn-vernon|
    * |ddd-distilled-vaughn-vernon|

.. warning:: **Protean** is currently under active development. APIs and interfaces are to be expected to change drastically and newer releases will almost certainly be backward incompatible. If you are interested in using Protean for your project, you may want to wait for the announcement of first stable production-ready version. If you want to use the framework *right now*, drop us an `email <subhash.bhushan@gmail.com>`_.

.. _key-features:

Key Features
------------

Protean is geared towards building multi-layered applications, that take advantage of the diverse options available at each level of the software stack.

- Very light framework footprint
- APIs that can be extended or overridden
- Non-opinionated and non-enforcing Application Code structure
- Abstract implementations for well-understood design patterns
- Expressive Domain Language for both developers as well as Business Users
- Full support for Domain-Driven Design, CQRS and Event Sourcing pattern implementations
- Utilities to write and maintain Living Documentation
- Support for a variety of SQL and NoSQL Databases
- Ready to use plugins for popular API frameworks like Flask and Pyramid
- Extendable interfaces to build custom plugins for the technology you want to use
- Container support for Docker *(Coming soon)*
- Kubernetes driven deployment mechanisms *(Coming soon)*
- Out-of-the-box support for deploying into AWS, Azure and GCP *(Coming soon)*

*Protean officially supports Python 3.7+.*

Guides
------

Protean guides contain a mixture of `Architecture Principles`, `Conventions`, `Practical Considerations`, `Protean Opinions/Choices` and `Sample code`. Wherever applicable, additional links to reference materials have been provided.

*Guides are not a replacement to these original texts. It is recommended that you go through them to hone and complete your DDD knowledge.*

.. toctree::
   :maxdepth: 1
   :caption: Principles

   philosophy/index
   blocks/index

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   user/foreword
   user/install
   user/quickstart
   user/composition-root
   user/identity
   user/domain-elements
   user/application-elements
   user/configuration
   user/persistence
   user/unit-of-work
   user/logging

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api/index

.. toctree::
   :maxdepth: 1
   :caption: Plugins

   plugins/api
   plugins/database
   plugins/broker


.. toctree::
   :maxdepth: 1
   :caption: Community

   community/changelog
   Code of Conduct <community/code-of-conduct>
   community/contributing


.. |ddd-eric-evans| raw:: html

    <a href="https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software-ebook/dp/B00794TAUG" target="_blank">Domain-Driven Design: Tackling Complexity in the Heart of Software - Eric Evans</a>

.. |implementing-ddd-vaughn-vernon| raw:: html

    <a href="https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon-ebook/dp/B00BCLEBN8" target="_blank">Implementing Domain-Driven Design - Vaughn Vernon</a>

.. |ddd-distilled-vaughn-vernon| raw:: html

    <a href="https://www.amazon.com/Domain-Driven-Design-Distilled-Vaughn-Vernon-ebook/dp/B01JJSGE5S" target="_blank">Domain-Driven Design Distilled - Vaughn Vernon</a>

.. |last-responsible-moment| raw:: html

    <a href="https://blog.codinghorror.com/the-last-responsible-moment/" target="_blank">Last Responsible Moment</a>
