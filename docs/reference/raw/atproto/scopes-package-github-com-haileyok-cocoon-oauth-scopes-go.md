# scopes package - github.com/haileyok/cocoon/oauth/scopes - Go Packages

> Source: https://pkg.go.dev/github.com/haileyok/cocoon/oauth/scopes
> Collected: 2026-10-23
> Published: Unknown
> Retrieval: HTTP GET, 2026-10-23; mode html; 1 response(s) archived in build/reference-wiki/http/pkg-go-dev-d9e5f23a/ (git-ignored): build/reference-wiki/http/pkg-go-dev-d9e5f23a/002.html (HTTP 200, sha256 e97196b9a7f5)
> Extraction: Main content extracted from HTML with BeautifulSoup + markdownify; scripts, navigation and footer chrome removed.
> Representation: Verbatim extraction of the source text (formatting noise removed)
> License: MIT — pkg.go.dev page lists License MIT; haileyok/cocoon LICENSE file is MIT
> Attribution: Copyright (c) 2025 me@haileyok.com, haileyok/cocoon (docs via pkg.go.dev)

## Documentation [¶](#section-documentation "Go to Documentation")

### Overview [¶](#pkg-overview "Go to Overview")

Package scopes parses and validates atproto OAuth permission scopes
(proposal 0011-auth-scopes). It models the granular resources (repo, rpc,
blob, account, identity, include) alongside the legacy static scopes
(atproto, transition:\*), and exposes enough structure for PAR-time validation
and resource-server enforcement.

### Index [¶](#pkg-index "Go to Index")

- [Constants](#pkg-constants)
- [Variables](#pkg-variables)
- [func ExpandSpaceCollections(ctx context.Context, r SpaceTypeResolver, grants []string) ([]string, error)](#ExpandSpaceCollections)
- [func SpaceCollectionsFromLexicon(doc map[string]any) ([]string, error)](#SpaceCollectionsFromLexicon)
- [func SpaceScopeNeededFor(t SpaceMatch) string](#SpaceScopeNeededFor)
- [type IndigoResolver](#IndigoResolver)
- - [func NewIndigoResolver() \*IndigoResolver](#NewIndigoResolver)
  - [func NewIndigoResolverWithDirectory(dir directory) \*IndigoResolver](#NewIndigoResolverWithDirectory)
  - [func NewIndigoResolverWithPLCURL(plcURL string) \*IndigoResolver](#NewIndigoResolverWithPLCURL)
- - [func (r \*IndigoResolver) ResolvePermissionSet(ctx context.Context, nsidStr string) (\*lexicon.SchemaPermissionSet, error)](#IndigoResolver.ResolvePermissionSet)
  - [func (r \*IndigoResolver) ResolveSpaceCollections(ctx context.Context, nsidStr string) ([]string, error)](#IndigoResolver.ResolveSpaceCollections)
  - [func (r \*IndigoResolver) ResolveSpacePermissions(ctx context.Context, nsidStr string) ([]\*SpacePermission, error)](#IndigoResolver.ResolveSpacePermissions)
- [type PermissionSetResolver](#PermissionSetResolver)
- [type Scope](#Scope)
- - [func Parse(raw string) (\*Scope, error)](#Parse)
  - [func ParseList(scope string) ([]\*Scope, error)](#ParseList)
- - [func (s \*Scope) AllowsAccount(attr, action string) bool](#Scope.AllowsAccount)
  - [func (s \*Scope) AllowsBlob(mediaType string) bool](#Scope.AllowsBlob)
  - [func (s \*Scope) AllowsIdentity(attr string) bool](#Scope.AllowsIdentity)
  - [func (s \*Scope) AllowsRepoWrite(collection, action string) bool](#Scope.AllowsRepoWrite)
- [type SpaceDeclaration](#SpaceDeclaration)
- - [func ParseSpaceDeclaration(doc map[string]any) (\*SpaceDeclaration, error)](#ParseSpaceDeclaration)
- [type SpaceMatch](#SpaceMatch)
- [type SpacePermission](#SpacePermission)
- - [func ParseSpacePermission(scope string) \*SpacePermission](#ParseSpacePermission)
  - [func SpacePermissionsFromLexicon(setNsid string, doc map[string]any) ([]\*SpacePermission, error)](#SpacePermissionsFromLexicon)
- - [func (p \*SpacePermission) HasCollections() bool](#SpacePermission.HasCollections)
  - [func (p \*SpacePermission) IsSelfAuthority() bool](#SpacePermission.IsSelfAuthority)
  - [func (p \*SpacePermission) Matches(t SpaceMatch) bool](#SpacePermission.Matches)
  - [func (p \*SpacePermission) String() string](#SpacePermission.String)
  - [func (p \*SpacePermission) WithDefaultCollections(collections []string) \*SpacePermission](#SpacePermission.WithDefaultCollections)
  - [func (p \*SpacePermission) WithResolvedAuthority(did string) \*SpacePermission](#SpacePermission.WithResolvedAuthority)
- [type SpacePermissionSetResolver](#SpacePermissionSetResolver)
- [type SpaceTypeResolver](#SpaceTypeResolver)

### Constants [¶](#pkg-constants "Go to Constants")

[View Source](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L18)

```
const (
	ResourceRepo       = "repo"
	ResourceRPC        = "rpc"
	ResourceBlob       = "blob"
	ResourceAccount    = "account"
	ResourceIdentity   = "identity"
	ResourceInclude    = "include"
	ResourceAtproto    = "atproto"
	ResourceTransition = "transition"
)
```

Resource identifiers for parsed scopes.

[View Source](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L12)

```
const ResourceSpace = "space"
```

ResourceSpace is the permissioned-data (Spaces) scope resource.

### Variables [¶](#pkg-variables "Go to Variables")

[View Source](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L16)

```
var SpaceActions = []string{"read_self", "read", "create", "update", "delete"}
```

SpaceActions lists the record actions in canonical order. read implies
read\_self.

[View Source](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L19)

```
var SpaceDefaultActions = []string{"read", "create", "update", "delete"}
```

SpaceDefaultActions applies when a grant names no action.

[View Source](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L22)

```
var SpaceManageOps = []string{"create", "update", "delete"}
```

SpaceManageOps lists the space-level management operations.

### Functions [¶](#pkg-functions "Go to Functions")

#### func [ExpandSpaceCollections](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L191) [¶](#ExpandSpaceCollections "Go to ExpandSpaceCollections") added in v0.13.1

```
func ExpandSpaceCollections(ctx context.Context, r SpaceTypeResolver, grants []string) ([]string, error)
```

ExpandSpaceCollections rewrites bare space:<type> grants to carry the
type's declared collections, as the reference's token issuance does.

A bare grant whose declaration can't be resolved is returned as it is, which
permits no writes, a narrower grant than the user consented to. The reference
refuses to issue such a token, so the first such failure is returned as an
error alongside the best-effort result, for callers that only display the
grants and can ignore it.

#### func [SpaceCollectionsFromLexicon](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L175) [¶](#SpaceCollectionsFromLexicon "Go to SpaceCollectionsFromLexicon") added in v0.13.1

```
func SpaceCollectionsFromLexicon(doc map[string]any) ([]string, error)
```

SpaceCollectionsFromLexicon reads the declared collections of a space type
lexicon document, after validating the whole declaration.

#### func [SpaceScopeNeededFor](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L328) [¶](#SpaceScopeNeededFor "Go to SpaceScopeNeededFor") added in v0.13.1

```
func SpaceScopeNeededFor(t SpaceMatch) string
```

SpaceScopeNeededFor is the narrowest grant that covers an operation, for an
insufficient-scope error.

### Types [¶](#pkg-types "Go to Types")

#### type [IndigoResolver](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L34) [¶](#IndigoResolver "Go to IndigoResolver")

```
type IndigoResolver struct {
	// contains filtered or unexported fields
}
```

IndigoResolver resolves permission sets using indigo's lexicon resolution
(DNS TXT `\_lexicon.<authority>` -> DID -> `com.atproto.lexicon.schema`
record), with a small in-memory TTL cache for both positive and negative
results.

#### func [NewIndigoResolver](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L46) [¶](#NewIndigoResolver "Go to NewIndigoResolver")

```
func NewIndigoResolver() *IndigoResolver
```

NewIndigoResolver builds a resolver backed by the default identity directory.

#### func [NewIndigoResolverWithDirectory](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L66) [¶](#NewIndigoResolverWithDirectory "Go to NewIndigoResolverWithDirectory")

```
func NewIndigoResolverWithDirectory(dir directory) *IndigoResolver
```

NewIndigoResolverWithDirectory builds a resolver using the supplied directory.

#### func [NewIndigoResolverWithPLCURL](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L53) [¶](#NewIndigoResolverWithPLCURL "Go to NewIndigoResolverWithPLCURL") added in v0.11.4

```
func NewIndigoResolverWithPLCURL(plcURL string) *IndigoResolver
```

NewIndigoResolverWithPLCURL builds a resolver backed by indigo's default
identity directory configuration, but resolving did:plc identities against
plcURL. An empty plcURL uses indigo's default PLC directory.

#### func (\*IndigoResolver) [ResolvePermissionSet](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L75) [¶](#IndigoResolver.ResolvePermissionSet "Go to IndigoResolver.ResolvePermissionSet")

```
func (r *IndigoResolver) ResolvePermissionSet(ctx context.Context, nsidStr string) (*lexicon.SchemaPermissionSet, error)
```

#### func (\*IndigoResolver) [ResolveSpaceCollections](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L20) [¶](#IndigoResolver.ResolveSpaceCollections "Go to IndigoResolver.ResolveSpaceCollections") added in v0.13.1

```
func (r *IndigoResolver) ResolveSpaceCollections(ctx context.Context, nsidStr string) ([]string, error)
```

ResolveSpaceCollections resolves a space type's declared collections.

#### func (\*IndigoResolver) [ResolveSpacePermissions](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_permission_set.go#L23) [¶](#IndigoResolver.ResolveSpacePermissions "Go to IndigoResolver.ResolveSpacePermissions") added in v0.13.1

```
func (r *IndigoResolver) ResolveSpacePermissions(ctx context.Context, nsidStr string) ([]*SpacePermission, error)
```

ResolveSpacePermissions resolves a permission set's space permissions.

#### type [PermissionSetResolver](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go#L17) [¶](#PermissionSetResolver "Go to PermissionSetResolver")

```
type PermissionSetResolver interface {
	ResolvePermissionSet(ctx context.Context, nsid string) (*lexicon.SchemaPermissionSet, error)
}
```

PermissionSetResolver resolves an `include:<nsid>` scope to its permission-set
lexicon. ResolvePermissionSet returns the parsed permission-set when the NSID
resolves to a valid permission-set record, or an error otherwise.

#### type [Scope](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L37) [¶](#Scope "Go to Scope")

```
type Scope struct {
	Raw      string
	Resource string

	// repo
	Collections []string
	Actions     []string

	// rpc
	Lxm []string
	Aud string

	// blob
	Accept []string

	// account / identity
	Attr   string
	Action string

	// include
	Nsid string

	// transition:<value>
	Transition string

	// space
	Space *SpacePermission
}
```

Scope is a single parsed scope token. Only the fields relevant to its
Resource are populated.

#### func [Parse](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L83) [¶](#Parse "Go to Parse")

```
func Parse(raw string) (*Scope, error)
```

Parse parses a single scope token, returning an error if it is syntactically
invalid or uses a disallowed wildcard combination.

#### func [ParseList](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L68) [¶](#ParseList "Go to ParseList")

```
func ParseList(scope string) ([]*Scope, error)
```

ParseList splits a space-delimited scope string and parses each token. It
returns an error on the first token that fails to parse.

#### func (\*Scope) [AllowsAccount](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L318) [¶](#Scope.AllowsAccount "Go to Scope.AllowsAccount") added in v0.11.2

```
func (s *Scope) AllowsAccount(attr, action string) bool
```

AllowsAccount checks attribute access; manage implies read.

#### func (\*Scope) [AllowsBlob](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L331) [¶](#Scope.AllowsBlob "Go to Scope.AllowsBlob") added in v0.11.2

```
func (s *Scope) AllowsBlob(mediaType string) bool
```

AllowsBlob reports whether this scope accepts a concrete MIME type.

#### func (\*Scope) [AllowsIdentity](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L326) [¶](#Scope.AllowsIdentity "Go to Scope.AllowsIdentity") added in v0.11.2

```
func (s *Scope) AllowsIdentity(attr string) bool
```

AllowsIdentity checks attribute access, including identity:\*.

#### func (\*Scope) [AllowsRepoWrite](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go#L295) [¶](#Scope.AllowsRepoWrite "Go to Scope.AllowsRepoWrite")

```
func (s *Scope) AllowsRepoWrite(collection, action string) bool
```

AllowsRepoWrite reports whether this scope grants the given repo write action
on the given collection. Non-repo scopes always return false.

#### type [SpaceDeclaration](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L64) [¶](#SpaceDeclaration "Go to SpaceDeclaration") added in v0.13.2

```
type SpaceDeclaration struct {
	// Key is the recommended space key type: any, nsid, tid or literal:<key>.
	Key string
	// Name is the human-readable name the consent screen shows (1-64 bytes).
	Name string
	// NameLang holds localized names by language tag.
	NameLang map[string]string
	// Description is for developers and is never shown to users.
	Description string
	// Collections are the default collections of a bare space: grant.
	Collections []string
}
```

SpaceDeclaration is a validated space type declaration: the defs.main of a
lexicon document with "type": "space".

#### func [ParseSpaceDeclaration](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L85) [¶](#ParseSpaceDeclaration "Go to ParseSpaceDeclaration") added in v0.13.2

```
func ParseSpaceDeclaration(doc map[string]any) (*SpaceDeclaration, error)
```

ParseSpaceDeclaration validates a lexicon document's main definition against
the space declaration schema the reference PDS applies: key, name and
collections are required, name is 1 to 64 bytes, name:lang maps language
tags to strings, and collections lists NSIDs (never a wildcard).

#### type [SpaceMatch](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L43) [¶](#SpaceMatch "Go to SpaceMatch") added in v0.13.1

```
type SpaceMatch struct {
	Type       string
	Authority  string
	Skey       string
	Action     string
	Collection string
	Manage     string
}
```

SpaceMatch is the operation a request needs: Action (with Collection for a
write) or Manage.

#### type [SpacePermission](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L32) [¶](#SpacePermission "Go to SpacePermission") added in v0.13.1

```
type SpacePermission struct {
	Type       string
	Authority  string
	Skey       string
	Collection []string // nil: no write targets
	Action     []string
	Manage     []string // nil: no manage operations
}
```

SpacePermission is a parsed `space:` scope, following SpacePermission in
@atproto/oauth-scopes (bluesky-social/atproto 5b95b2f2):

```
space:<type>?authority=<did|self|*>&skey=<rkey|*>&collection=<nsid|*>&action=..&manage=..
```

Authority defaults to "self", resolved to the granting user's DID when a
token is issued; an unresolved "self" matches nothing. A grant without a
collection permits no writes.

#### func [ParseSpacePermission](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L91) [¶](#ParseSpacePermission "Go to ParseSpacePermission") added in v0.13.1

```
func ParseSpacePermission(scope string) *SpacePermission
```

ParseSpacePermission parses a `space:` scope, returning nil when it is not
one or is invalid.

#### func [SpacePermissionsFromLexicon](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_permission_set.go#L62) [¶](#SpacePermissionsFromLexicon "Go to SpacePermissionsFromLexicon") added in v0.13.1

```
func SpacePermissionsFromLexicon(setNsid string, doc map[string]any) ([]*SpacePermission, error)
```

SpacePermissionsFromLexicon reads the space permissions of a permission
set lexicon document, as the reference's IncludeScope does: each becomes a
space: grant, and only space types under the set's own NSID authority are
kept. Invalid entries are skipped.

#### func (\*SpacePermission) [HasCollections](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L221) [¶](#SpacePermission.HasCollections "Go to SpacePermission.HasCollections") added in v0.13.1

```
func (p *SpacePermission) HasCollections() bool
```

HasCollections reports whether the grant names write collections.

#### func (\*SpacePermission) [IsSelfAuthority](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L224) [¶](#SpacePermission.IsSelfAuthority "Go to SpacePermission.IsSelfAuthority") added in v0.13.1

```
func (p *SpacePermission) IsSelfAuthority() bool
```

IsSelfAuthority reports whether the authority is the unresolved "self".

#### func (\*SpacePermission) [Matches](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L195) [¶](#SpacePermission.Matches "Go to SpacePermission.Matches") added in v0.13.1

```
func (p *SpacePermission) Matches(t SpaceMatch) bool
```

Matches reports whether the grant covers an operation.

#### func (\*SpacePermission) [String](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L272) [¶](#SpacePermission.String "Go to SpacePermission.String") added in v0.13.1

```
func (p *SpacePermission) String() string
```

String formats the grant canonically, leaving out defaults.

#### func (\*SpacePermission) [WithDefaultCollections](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L228) [¶](#SpacePermission.WithDefaultCollections "Go to SpacePermission.WithDefaultCollections") added in v0.13.1

```
func (p *SpacePermission) WithDefaultCollections(collections []string) *SpacePermission
```

WithDefaultCollections materializes a space type's declared collections
into a grant that names none.

#### func (\*SpacePermission) [WithResolvedAuthority](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go#L238) [¶](#SpacePermission.WithResolvedAuthority "Go to SpacePermission.WithResolvedAuthority") added in v0.13.1

```
func (p *SpacePermission) WithResolvedAuthority(did string) *SpacePermission
```

WithResolvedAuthority resolves a "self" authority to the user's DID.

#### type [SpacePermissionSetResolver](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_permission_set.go#L18) [¶](#SpacePermissionSetResolver "Go to SpacePermissionSetResolver") added in v0.13.1

```
type SpacePermissionSetResolver interface {
	ResolveSpacePermissions(ctx context.Context, nsid string) ([]*SpacePermission, error)
}
```

SpacePermissionSetResolver resolves the space permissions an include:
permission set grants. Permission sets may hold space permissions
({"resource": "space", "spaceType": ..., "authority", "skey", "collection",
"action", "manage"}), which indigo's permission-set schema doesn't model.

#### type [SpaceTypeResolver](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go#L15) [¶](#SpaceTypeResolver "Go to SpaceTypeResolver") added in v0.11.1

```
type SpaceTypeResolver interface {
	ResolveSpaceCollections(ctx context.Context, nsid string) ([]string, error)
}
```

SpaceTypeResolver resolves a space type NSID to the collections its
lexicon declaration ({"type": "space", "collections": [...]}) names.

## Source Files [¶](#section-sourcefiles "Go to Source Files")

[View all Source files](https://github.com/haileyok/cocoon/tree/v0.13.3/oauth/scopes)

- [parser.go](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/parser.go "parser.go")
- [resolver.go](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/resolver.go "resolver.go")
- [space.go](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space.go "space.go")
- [space\_permission\_set.go](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_permission_set.go "space_permission_set.go")
- [space\_resolver.go](https://github.com/haileyok/cocoon/blob/v0.13.3/oauth/scopes/space_resolver.go "space_resolver.go")

Click to show internal directories.

Click to hide internal directories.


## License notice (verbatim, from https://raw.githubusercontent.com/haileyok/cocoon/main/LICENSE)

```
MIT License

Copyright (c) 2025 me@haileyok.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
