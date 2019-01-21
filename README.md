# django-mini-cms

The minimalist cms, with four plugable core modules. That are

- (basic implementation done) A toolbar for your frontend, allows login/logout, and model editing directly in the frontend
- (to be done) A dynamic content framework, for hierarchical content on any model, always based on the same content types
- (to be done) A page tree module, for building, yes, page trees
- (to be done, last) A publisher module, for adding a basic live/draft version separation, where the draft can then be published to live. for any model that wants it

All three are optional, whereas the toolbar is probably needed in most cases.

This project is inspired by django-cms, but tries to avoid any magic and over complex things.
