Changelog
=========

0.7.2 (2020-09-14)
------------------

- WEB-3355: Fix `aria-expanded` property when the menu is closed
  [mpeeters]


0.7.1 (2020-08-24)
------------------

- Release.
  [bsuttor]


0.7.0 (2020-08-24)
------------------

- New release (Previous failed)
  [boulch]


0.7.0b3 (2020-08-24)
--------------------

- WEB-3355 : Improve menu accessibility by adding `aria-expanded` property
  [mpeeters]


0.7.0b2 (2020-06-04)
--------------------

- WEB-3329: Improve accessibility for menu by :
  - Setting the focus on the first element of the submenu
  - When using back tab or upper arrow on first submenu entry, setting the focus back to the first navigation level
  - When using tab or down arrow on last submenu entry, setting the focus to the next entry of the first navigation level
  [mpeeters]

- WEB-3329: tabindex must be always equal to zero to respect natural order for accessibility
  [mpeeters]


0.7.0b1 (2020-05-28)
--------------------

- WEB-3329: Set the focus on the submenu when the first level is clicked
  [mpeeters]

- WEB-3329: Revert Improve accessibility by opening first level menu links on enter
  [mpeeters]

- Remove tabindex on globalnav
  [mpeeters]


0.6.9 (2020-05-26)
------------------

- WEB-3329: Improve accessibility by opening first level menu links on enter
  [mpeeters]

- Moved these translations into cpskin.locales package
  [macagua]

- Add more improvements for i18n support
  [macagua]


0.6.8 (2019-07-16)
------------------

- Support of target_blank / target = "_blank" href property on a link portal_type.
  . Avoid opening target in a blank windows when user have permission to modify portal content.
  . update test
  [cboulanger]


0.6.7 (2019-04-08)
------------------

- Invalidate menu cache when current, old or new workflow state is published_and_shown.
  [bsuttor]


0.6.6 (2019-02-11)
------------------

- Handle special cases when we don't get a request at ObjectAddedEvent
  (example : when an object is added at Zope startup)
  [laulaz]


0.6.5 (2018-01-22)
------------------

- Try except `api.portal.get()`, there is no plone site when plone site is installed.
  [bsuttor]


0.6.4 (2018-01-03)
------------------

- Bad release.
  [bsuttor]


0.6.3 (2018-01-03)
------------------

- Check WorkflowException when invalidate cache for testing.
  [bsuttor]


0.6.2 (2017-12-20)
------------------

- Invalidate menu only if obj is published_and_shown.
  [bsuttor]


0.6.1 (2017-12-20)
------------------

- Delete underline to portal-globalnav-cpskinmenu .selected a,
  .portal-globalnav-cpskinmenu-tabs .selected a,
  .portal-globalnav-cpskinmenu .navTreeItemInPath > span a
  [mgennart]


0.6.0 (2017-10-06)
------------------

- First click on top menu item opens its submenu,
  second click on top menu item closes its submenu.
  [gotcha]

- Add 'menu-activated' class on opened menu <li>
  [laulaz]


0.5.3 (2017-09-20)
------------------

- Add conditionnal description on portal tabs : #17333
  [laulaz]


0.5.2 (2017-08-25)
------------------

- Hide advanced breadcrumbs when loading page
  [gotcha]

- Sort Direct Access links alphabetically
  [laulaz]


0.5.1 (2016-09-16)
------------------

- Fix menu items in the path
  [gotcha]


0.5.0 (2016-08-09)
------------------

- Move CPSkin actions to a new dedicated menu
  [laulaz]


0.4.10 (2016-07-04)
-------------------

- No menu should be opened when accessing root of the portal.
  [gotcha]


0.4.9 (2016-06-29)
------------------

- Menu should be based on navigation root.
  [gotcha]


0.4.8 (2016-06-29)
------------------

- Finer grained cachekey on domain and language
  [jfroche, gotcha]


0.4.7 (2016-06-22)
------------------

- Fix open/close of top level submenu for mobile
  [gotcha]


0.4.6 (2016-06-16)
------------------

- Tune mobile menu CSS
  [mgennart]

- Add tests without any caching to debunk issues with caching.
  [gotcha]

- Mobile menu should not load a page when at first level folders,
  but rather open next submenu.
  [gotcha]

- Tune caching.
  [gotcha]

- Move some computation from server to client to improve caching.
  [gotcha]


0.4.5 (2016-03-08)
------------------

- Fix `Unicode Decode Error` in vocabulary.
  [bsuttor]

- Fixing cpskin.policy tests.
  [bsuttor]

- Fixing tests.
  [bsuttor, schminitz]


0.4.4 (2015-09-29)
------------------

- Add persistence to submenu using cpskin parameter (affinitic #6267)
  [schminitz]

0.4.3 (2015-09-28)
------------------

- Close level 2 menu on outside click.
  [schminitz]


0.4.2 (2015-08-18)
------------------

- New way to get if multilingual site or not for vocabulary. Indeed, plone.app.multilingual
  may be in buildout but not installed on Plone.
  [bsuttor]


0.4.1 (2015-03-17)
------------------

- Fix last level menu vocabulary for multilingual websites : #10397
  [mpeeters]


0.4.0 (2015-03-05)
------------------

- Load submenu js into javascript_registry IMIO refs #9878


0.3.3 (2014-11-18)
------------------

- Fix mobile error.


0.3.2 (2014-10-22)
------------------

- Fix override zcml error.


0.3 (2014-10-07)
----------------

- Remove MenuTools viewlet (affinitic #6023)
- Remove Â» in menu (affinitic #6025)
- Move media menu.css in menu_mobile.css [FBruynbroeck]


0.2 (2014-08-21)
----------------

- Add a vocabulary for the last level navigation [mpeeters]


0.1 (2014-07-02)
----------------

- Change desktop menu behaviour. [giacomos]
- Change mobile menu behaviour clicking on third level. [lucabel]
- Switch between mobile view and desktop view only with css media query. [lucabel]
