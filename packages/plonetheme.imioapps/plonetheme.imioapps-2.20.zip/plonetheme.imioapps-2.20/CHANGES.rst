Changelog
=========


2.20 (2020-09-07)
-----------------

- plonemeetingskin : increase base line-height as font-size was increased.
  [gbastien]

2.19 (2020-09-01)
-----------------

- Fix input text/passowrd and textarea background-color so default styles
  applied by Firefox are overrided (Firefox 80+).
  [gbastien]

2.18 (2020-08-18)
-----------------

- imioapps : style the `PloneGroupUsersGroupsColumn` column.
  [gbastien]
- plonemeetingskin : make sure very large images are not
  exceeding the screen.
  [gbastien]
- plonemeetingskin : removed useless styles about `actionMenuAX`
  that was replaced by `tooltipster`.
  [gbastien]
- imioapps : make sure input submit/button use `cursor:pointer`, moreover
  fix Firefox disappearance of `outline` when an `input submit` is clicked,
  replace it with a `box-shadow` as we use `border-radius`.
  [gbastien]
- imioapps : remove multiple definition for `#content legend padding`.
  [gbastien]

2.17 (2020-06-24)
-----------------

- plonemeetingskin : moved rules with logic to hide something
  back to plonemeting.css
  [gbastien]
- Make sure tooltipster tooltip arrow is displayed correctly
  (stay sticked to the tooltipster) when zooming in the internet browser.
  [gbastien]

2.16 (2020-04-02)
-----------------

- Added configurable help icon on the site header
  [sdelcourt]
- More precise CSS selector to hide CKEditor's spellchecking ad.
  [gbastien]

2.15 (2020-03-12)
-----------------

- Avoid too much padding top and left in CKeditor edit zone.
  [gbastien]
- Added a new CSS rule to hide CKEditor's spellchecking ad [aduchene]

2.14 (2020-02-06)
-----------------

- plonemeetingskin : added icon for 'wait advices' WF action panel button.
  [gbastien]

2.13 (2020-01-10)
-----------------

- As state color is defined on `<span>` with `imio.prettylink`,
  define `linkColor` on hover.
  [gbastien]

2.12 (2019-10-14)
-----------------

- Use common CSS for workflowstate viewlet.
  [gbastien]

2.11 (2019-09-12)
-----------------

- Added style for apButtonSelect class of actionspanel.
  [sgeulette]
- Added CSS for datagridfield rendered in a dashboard additional infos column.
  [gbastien]
- Added workflowstate viewlet
  [sgeulette]
- Added css for apButtonAction_edit.
  [sgeulette]

2.10 (2019-06-28)
-----------------

- Set `collective.behavior.talcondition` input field `width` to `99%`.
  [gbastien]

2.9 (2019-06-08)
----------------

- Set `padding-top: 0.5em;` instead `padding-top: 1em;` for
  `td.table_widget_value` so it is the same value as for
  `td.table_widget_label` and label/value are correctly aligned in views
  using it (our default dexterity view).
  [gbastien]

2.8 (2019-05-16)
----------------

- Added spinner_small.gif image and use it in the async_actions_panel div.
  [gbastien]
- Purge and redefine bundles used by resources registries
  (portal_css/portal_javascripts).
  [gbastien]
- Make sure a:visited links in portlets have same color as a:link.
  [gbastien]
- As header's height is `position:fixed`, compute the `#emptyviewlet`'s height
  dynamically using JS.  Viewlet's height is computed by calling the JS method
  directly in `empty.pt` so we do not see viewlet size changing.
  [gbastien]
- If current URL contains `imio-test`, highlight `portal-header` (turn it red).
  [gbastien]
- Override the `plone_context_state` view to redefine `canonical_object_url`
  to strip the `URL` containing `portal_factory` as this URL is used to call
  asynchronous JS functions.
  [gbastien]

2.7 (2019-01-28)
----------------

- pst css.
  [sgeulette]

2.6 (2019-01-25)
----------------

- imioapps : fixed fieldset legend height to 18px.
  [gbastien]
- plonemeetingskin : added icon for 'reorder items' action panel button.
  [gbastien]

2.5 (2018-12-18)
----------------

- imioapps : limit margin-bottom under fieldset.
  [gbastien]
- plonemeetingskin : remove margin under table displaying item infos
  on the item view.
  [gbastien]

2.4 (2018-12-04)
----------------

- plonemeetingskin : do not define border for .enableFormTabbing on
  faceted navigation.
  [gbastien]

2.3 (2018-11-29)
----------------

- Make sure dotted bottom border is displayed when using class 'link-tooltip'
  and element is used in a table.listing because base.css removes border-bottom
  using a !important...
  [gbastien]

2.2 (2018-11-20)
----------------

- Do not use `"` in dtml `fontFamily` property from `imioapps_properties.props`
  or it can not be used in `dtml`, used `'` instead.
  [gbastien]
- Skin `Add contact` link at bottom of `collective.contact.core` organization
  view so it is isolated from linked contacts and displayed correctly when
  using an actions panel viewlet at the bottom of the page.
  [gbastien]
- Set relative position on header in manage-viewlets view
  [sgeulette]
- Skin `collective.contact.core` `tooltip` to manage fixed width and correct
  display when `tooltip` content is too long.
  [gbastien]
- Skin z3c.form datagridfield to indentify row content.
  [gbastien]
- Added css to style as list li tag in overlay link integrity delete confirmation
  [sgeulette]
- Increase height of dropdown list of querystring dropdown widget
  (Collection query field widget).
  [gbastien]
- Be more precise about label for which bold is removed, only apply to
  multiselection lists of DX and AT.
  [gbastien]
- Adapted to not use position:absolute for fieldset legend.
  [gbastien]

2.1 (2018-07-23)
----------------

- Fix header so it is always visible.
  [gbastien]
- Depends on `collective.messagesviewlet` as we override the viewlet to move it
  from `IPortalHeader` to `IPortalTop` viewletmanager.
  [gbastien]
- Updated spinner.gif image to fit with skin default colors.
  [gbastien]
- Removed left-padding for #portal-globalnav.
  [gbastien]

2.0.17 (2018-04-20)
-------------------

- Limit padding for tooltipstered content.
  [gbastien]

2.0.16 (2018-02-23)
-------------------

- Adapted to new styles of tooltipster 4.2.6.
  [gbastien]

2.0.15 (2018-01-30)
-------------------

- Skin column-two the same way as column-one.  This makes portlets displayed
  on the left or on the right look similar.
  [gbastien]
- Hide borders of tables using class `no-style-table`.
  [gbastien]

2.0.14 (2017-12-07)
-------------------

- Only display the `scan` tab on annexes to roles `Manager/MeetingManager`.
  [gbastien]

2.0.13 (2017-11-28)
-------------------

- Set `vertical-align: bottom` for `input` instead `vertical-align: text-top`
  for `label` to align `input` and `label` correctly.
  [gbastien]

2.0.12 (2017-11-24)
-------------------

- Added favicon.
  [sgeulette]
- Skin `input#form-buttons-cancel` the same way `input.standalone` and skin
  `collective.eeafaceted.batchactions` buttons the same way `imio.actionspanel`
  buttons.
  [gbastien]

2.0.11 (2017-10-05)
-------------------

- Display navigation portlet same way as other portlets.
  [gbastien]
- Display the infos in the CKeditor SCAYT WebSpellChecker popup correctly.
  [gbastien]

2.0.10 (2017-08-30)
-------------------

- Removed styling for class `form.apFormButton` as it was removed from
  imio.actionspanel 1.29+, the add content select now uses the standard
  `apButton` CSS class like other buttons.
  [gbastien]
- Skin portletFooter to align it right.
  [gbastien]

2.0.9 (2017-08-28)
------------------

- Added icon for the store_every_items_decision_as_annex action
  in the plonemeetingskin.
  [gbastien]
- Fixed fieldset/legend top padding.

2.0.8 (2017-06-09)
------------------

- Make <abbr> and <acronym> dotted underline work for every browsers.
  [gbastien]
- Removed useless code about MeetingFile in plonemeetingskin.
  [gbastien]
- Display <th> of table the same way as it is rendered by appy.pod, namely text
  black and grey background.
  [gbastien]

2.0.7 (2017-03-22)
------------------

- Use a brighter blue color for links.
  [gbastien]

2.0.6 (2017-03-14)
------------------

- Highlight the 'lost password?' link in the login_form.
- Style actionspanel select button
- Adapted styles so font-size and line-height are the same while using CKeditor
- Added file imioapps_ckeditor_moonolisa.css.dtml that is enabled when the
  Moono-Lisa skin is selected in CKEditor properties.  This makes it work
  correctly in Chrome and greyed a bit more the selected buttons
- Reduce fieldset padding in form fieldset tabbing

2.0.5 (2017-01-25)
------------------

- Do not use 'float: left;' to move the <legend> tag, it is not working
  anymore with recent versions of Chrome.  Instead use 'position: absolute;'.
  This works in both FF and Chrome and simplify overal CSS.
- Display AT and DX field title bold but selectable contents as normal.
  This is the case for radio buttons, multiple checkboxes, ...

2.0.4 (2016-12-05)
------------------

- Added margin-left for listingBar 'next elements' button or it sticks
  to previous one. This appears until Plone 4.3.8.
- Update pstskin profile (reduce logo, change css)


2.0.3 (2016-06-17)
------------------

- Removed styling for tags <acronym> and <abbr>.
- Optimized icon position on buttons.
- Small fixes for Chrome.


2.0.2 (2016-05-17)
------------------

- Display header correctly for anonymous when portal_tabs are displayed.
- Removed padding-left added by Firefox to input.
- Skin portlet News.


2.0.1 (2016-05-13)
------------------

- Use navBackgroundColor for listingBar hover and select color.
- Make sure broken images are shown in FF.
- Display default faceted widgets (not advanced) the same height.


2.0 (2016-04-19)
----------------

- New layout.


1.2.7 (2016-01-21)
------------------

- Removed 'meetingadvice' icon relevant CSS as it uses a real icon now.
- Define 'height' for search button so it is displayed correctly in Chrome.
- Added left/right padding to collective.messagesviewlet message.
- Limit padding in z3ctable header cells.


1.2.6 (2015-12-03)
------------------

- imioapps : use a bigger spinner.gif and grey page when faceted is locked

1.2.5 (2015-07-14)
------------------

- Several adaptations regarding imio.dashboard integration

1.2.4 (2015-03-18)
------------------
- plonemeetingskin : do not display a contenttype-x icon for type 'MeetingFile' and 'MeetingItem'
- imioapps : skin also listingBar displayed in referencebrowserwidget

1.2.3 (2014-09-23)
------------------
- Added back skins.zcml that register File System Directory Views
- Added profile to go to version 1.2.3 that removes old _templates File System Directory Views

1.2.2 (2014-09-23)
------------------
- Nothing changed yet.

1.2.1 (2014-09-23)
------------------
- Nothing changed yet.

1.2 (2014-09-22)
----------------
- Nothing yet

1.1 (2014-03-07)
----------------
- Adapted styles

1.0 (2014-02-12)
----------------
- First release, added 4 skins : dmsmailskin, imioapps, plonemeetingskin, pstskin
