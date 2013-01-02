TracTicketLimitPlugin
=====================

Trac plugin to limit ticket creation to a fixed number per day per user.

Plugin developed for [Missing Pixel Studios, Inc.](http://www.missingpixelstudios.com/ "Missing Pixel Studios") by [BitStruct, LLC](http://www.bitstruct.com "BitStruct, LLC").

Install
-------

console# ./setup.py install

Source
------

The source is available from:
http://github.com/bitstruct/TracTicketLimitPlugin

Configuration
-------------

Configure by enabling the tracticketlimit Trac component in the ini.

Create a section called [limited_tickets].
Add an entry for the timezone to use as a base for the start of the day.
List out components that need limits.

Example:

[components]
tracticketlimit = enabled

[limited_tickets]
timezone = US/Pacific
component_limits = Color Suggestions:1, Object Suggestions:2


License
-------
Copyright (c) 2012, Missing Pixel Studios, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this software except in compliance with the License.  You
may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.

