Cased Guard Protocol Specification
======================================
Author: Cased, Inc.


**1: Introduction**

The Cased Guard Protocol ("Cased Protocol", or "CP") is a
technology-agnostic, format-agnostic process for the approval or denial
of actions via approved _sessions_ (that can optionally
extend over time), with a single scope (an "application") that defines
that session. Because sessions can also have "one-off" approvals,
with no extension over time, the protocol can also be used to approve
a single action, with just the scope of that action approved.

The Cased Protocol also includes configurable options that define
these sessions, as well as settings to account for certain
communication failure conditions between the requestor and the receiver.


**1.1: Glossary**

* _application_:      An entity associated with approval requests.
* _client_:           The initiatior of a session request
* _server_:           The receiver of a session request
* _session_:          A state of approval permitting actions to occur,
                      with an optional duration of time
* _session request_:  A request for approval, which is granted via a session


**2: Pre-Request Configuration**

Before sending session requests, the client SHOULD receive and store a small set of
configuration metadata from the server. If this data exists, it MUST
be available for each application. It MAY exist as a general setting
for all applications, or be set per-application. This data MUST include:

* _applications_:         A list of identifiers for every application that the server will accept.
* _deny_if_unreachable_:  Deny any request if the server cannot be reached. This
                          can be set per-application, or in general.


**3: Requests**

A _guard request_ is initiated by an actor. It MUST include the following data:

* _application_: an identifier of the application scope
* _requestor_:   an identifier of the actor/entity making the request

If _reason_required_ has been set (see section 5), the request MUST include:

* _reason_: The reason for the request

Additionally, servers MUST automatically deny requests that do not
include a reason, if so configured. Servers SHOULD prompt clients to then
send a reason. Clients SHOULD allow a follow-up request including the reason.

The request MAY include additional metadata. The goal of this metadata is to
give the receiver as much information as possible to make the correct
approval/denial decision.


**4: Approvals and Denials**

The format of an approval or denial response is not specified, and is
dependent on client implementation. However it MUST give the client sufficient
information to proceed with its operations. Additionally, a response (either
approval or denial) MUST be given within a _session_request_timeout_
(see section 5).


**5: Settings For Sessions**

The server controls a set of configuration options that govern sessions.
These MUST include:


* _reason_required_:           A boolean indicating whether a reason is required for approval. This
                               can be set per-application, or in general.

* _session_approval_duration_: If a requestor is approved for a session, how long
                               subsequent requests (for that application)
                               will be automatically approved. If set to 0, then
                               the session has no extension in time (i.e. it is a
                               "one-off" approval).

* _session_request_timeout_:   If a request is not approved within this limit, the
                               session request will be denied.



