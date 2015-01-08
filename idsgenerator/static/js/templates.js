angular.module('MainApp').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('src/js/templates/idsGenerator.html',
    "<div class=\"col-md-12\">\n" +
    "    <h1> IDS Generator</h1>\n" +
    "</div>\n" +
    "\n" +
    "<form role='form' method=\"POST\" ng-submit=\"submit()\">\n" +
    "\n" +
    "        <div class='col-md-6'>\n" +
    "        <table id=\"us_patent_table\" class=\"table\">\n" +
    "            <thead>\n" +
    "            <tr><td colspan=\"3\">U.S PATENTS</td></tr>\n" +
    "            <tr>\n" +
    "                <td>Patent Number</td>\n" +
    "                <td>Issue Date</td>\n" +
    "                <td>First Named Inventor</td>\n" +
    "            </tr>\n" +
    "            </thead>\n" +
    "                <tr class=\"us_patent_row\" ng-repeat=\"usPatentRow in usPatentRows\">\n" +
    "                  <td><div class=\"form-group\"><input ng-model=\"usPatentRow.number\" ng-blur=\"fillInUsPatentData(usPatentRow)\" type=\"text\" class=\"form-control us_patent\" name=\"us_patent\"></div></td>\n" +
    "                  <td><div class=\"form-group\"><input ng-model=\"usPatentRow.date\" type=\"text\" class=\"form-control us_patent_date\" name=\"us_patent_date\"></div></td>\n" +
    "                  <td><div class=\"form-group\"><input ng-model=\"usPatentRow.inventor\" type=\"text\" class=\"form-control us_patent_inventor\" name=\"us_patent_inventor\"></div></td>\n" +
    "                </tr>\n" +
    "                <tr>\n" +
    "                    <td colspan=\"3\">\n" +
    "                        <button type=\"button\" class=\"btn btn-default\" ng-click=\"addUsPatentRow(1)\">Add Row</button>\n" +
    "                        <button type=\"button\" class=\"btn btn-default\" ng-click=\"addUsPatentRow(5)\">Add 5 Rows</button>\n" +
    "                    </td>\n" +
    "                </tr>\n" +
    "        </table>\n" +
    "\n" +
    "        <table id=\"us_application_table\" class=\"table\">\n" +
    "            <thead>\n" +
    "            <tr><td colspan=\"3\">U.S APPLICATIONS</td></tr>\n" +
    "            <tr>\n" +
    "                <td>Application Numbers</td>\n" +
    "                <td>Issue Date</td>\n" +
    "                <td>First Named Applicant</td>\n" +
    "            </tr>\n" +
    "            </thead>\n" +
    "                <tr class=\"us_application_row\" ng-repeat=\"usApplicationRow in usApplicationRows\">\n" +
    "                  <td><div class=\"form-group\"><input ng-model=usApplicationRow.number ng-blur=\"fillInUsApplicationData(usApplicationRow)\" type=\"text\" class=\"form-control us_application\" name=\"us_application\"></div></td>\n" +
    "                  <td><div class=\"form-group\"><input ng-model=usApplicationRow.date type=\"text\" class=\"form-control us_application_date\" name=\"us_application_date\"></div></td>\n" +
    "                  <td><div class=\"form-group\"><input ng-model=usApplicationRow.inventor type=\"text\" class=\"form-control us_application_applicant\" name=\"us_application_inventor\"></div></td>\n" +
    "                </tr>\n" +
    "            <tr>\n" +
    "                <td colspan=\"3\">\n" +
    "                    <button type=\"button\" class=\"btn btn-default\" ng-click=\"addUsApplicationRow(1)\">Add Row</button>\n" +
    "                    <button type=\"button\" class=\"btn btn-default\" ng-click=\"addUsApplicationRow(5)\">Add 5 Rows</button>\n" +
    "                </td>\n" +
    "            </tr>\n" +
    "        </table>\n" +
    "\n" +
    "        <table id=\"foreign_application_table\" class=\"table\">\n" +
    "            <thead>\n" +
    "            <tr><td colspan=\"3\">FOREIGN APPLICATION</td></tr>\n" +
    "            <tr>\n" +
    "                <td>Application Numbers</td>\n" +
    "                <td>Issue Date</td>\n" +
    "                <td>First Named Applicant</td>\n" +
    "            </tr>\n" +
    "            </thead>\n" +
    "            <tr class=\"foreign_application_row\" ng-repeat=\"foreignApplicationRow in foreignApplicationRows\">\n" +
    "              <td><div class=\"form-group\"><input ng-model=foreignApplicationRow.number ng-blur=\"fillInForeignApplicationData(foreignApplicationRow)\" type=\"text\" class=\"form-control foreign_application\" name=\"foreign_application\"></div></td>\n" +
    "              <td><div class=\"form-group\"><input ng-model=foreignApplicationRow.date type=\"text\" class=\"form-control foreign_application_date\" name=\"foreign_application_date\"></div></td>\n" +
    "              <td><div class=\"form-group\"><input ng-model=foreignApplicationRow.inventor type=\"text\" class=\"form-control foreign_application_applicant\" name=\"foreign_application_inventor\"></div></td>\n" +
    "            </tr>\n" +
    "            <tr>\n" +
    "                <td colspan=\"3\">\n" +
    "                    <button type=\"button\" class=\"btn btn-default\" ng-click=\"addForeignApplicationRow(1)\">Add Row</button>\n" +
    "                    <button type=\"button\" class=\"btn btn-default\" ng-click=\"addForeignApplicationRow(5)\">Add 5 Rows</button>\n" +
    "                </td>\n" +
    "            </tr>\n" +
    "        </table>\n" +
    "\n" +
    "        <table id=\"non_patent_table\" class=\"table\">\n" +
    "            <thead>\n" +
    "            <tr>\n" +
    "                <td>NON PATENT LITERATURE</td>\n" +
    "            </tr>\n" +
    "            </thead>\n" +
    "                <tr class=\"non_patent_row\" ng-repeat=\"nonPatentRow in nonPatentRows track by $index\">\n" +
    "                  <td><div class=\"form-group\"><input ng-model=\"nonPatentRow.text\" type=\"text\" class=\"form-control non_patent\" name=\"non_patent\"></div></td>\n" +
    "                </tr>\n" +
    "                <tr>\n" +
    "                    <td>\n" +
    "                        <button type=\"button\" class=\"btn btn-default\" ng-click=\"addNonPatentRow(1)\">Add Row</button>\n" +
    "                        <button type=\"button\" class=\"btn btn-default\" ng-click=\"addNonPatentRow(5)\">Add 5 Rows</button>\n" +
    "                    </td>\n" +
    "                </tr>\n" +
    "        </table>\n" +
    "\n" +
    "        <div class=\"checkbox\">\n" +
    "         <label><input type=\"checkbox\" ng-click=\"updateAllCitedSelection()\" ng-model=\"each_item_cited\">That each item of information contained in the information disclosure statement was first cited in any\n" +
    "         communication from a foreign patent office in a counterpart foreign application not more than three months prior\n" +
    "         to the filing of the information disclosure statement. See 37 CFR 1.97(e)(1).</label>\n" +
    "       </div>\n" +
    "\n" +
    "       <div class=\"checkbox\">\n" +
    "         <label><input type=\"checkbox\" ng-click=\"updateNoCitedSelection()\" ng-model=\"no_item_cited\">That no item of information contained in the information disclosure statement was cited in a communication from\n" +
    "         a foreign patent office in a counterpart foreign application, and, to the knowledge of the person signing the\n" +
    "         certification after making reasonable inquiry, no item of information contained in the information disclosure\n" +
    "         statement was known to any individual designated in 37 CFR 1.56(c) more than three months prior to the filing of\n" +
    "         the information disclosure statement. See 37 CFR 1.97(e)(2).</label>\n" +
    "       </div>\n" +
    "\n" +
    "        <div class=\"checkbox\">\n" +
    "          <label><input type=\"checkbox\" ng-model=\"certification_attached\">See attached certification statement.</label>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"checkbox\">\n" +
    "          <label><input type=\"checkbox\" ng-model=\"fee_submitted\">The fee set forth in 37 CFR 1.17 (p) has been submitted herewith.</label>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"checkbox\">\n" +
    "          <label><input type=\"checkbox\" ng-model=\"certification_not_submitted\">A certification statement is not submitted herewith.</label>\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <label for=\"signature_name\">Name:</label>\n" +
    "          <input type=\"text\" class=\"form-control\" id=\"signature_name\" ng-model=\"signature_name\" ng-change=\"signature_name_changed\">\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <label for=\"signature_name\">Signature:</label>\n" +
    "          <input type=\"text\" class=\"form-control\" id=\"signature_name\" ng-model=\"signature\" ng-change=\"signature_changed\">\n" +
    "        </div>\n" +
    "\n" +
    "        <div class=\"form-group\">\n" +
    "          <label for=\"signature_registration_number\">Registration Number:</label>\n" +
    "          <input type=\"text\" class=\"form-control\" id=\"signature_registration_number\" ng-model=\"signature_registration_number\">\n" +
    "        </div>\n" +
    "\n" +
    "        <button type=\"submit\" class=\"btn btn-lg btn-primary\">Submit</button>\n" +
    "        </div>\n" +
    "\n" +
    "\n" +
    "        <div class=\"col-md-4\">\n" +
    "            <strong><em> {{ loading_message }} </em></strong>\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"application_number\">Application Number:</label>\n" +
    "              <input ng-model=\"application\" ng-blur=\"fillInApplicationData(application)\"  type=\"text\" class=\"form-control\" id=\"application_number\" name=\"application_number\">\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"filing_date\">Filing Date:</label>\n" +
    "              <input ng-disabled=\"loading_application_data\" ng-model=\"filing_date\" type=\"text\" class=\"form-control\" id=\"filing_date\" name=\"filing_date\">\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"first_named_inventor\">First Named Inventor:</label>\n" +
    "              <input ng-disabled=\"loading_application_data\" ng-model=\"first_named_inventor\" type=\"text\" class=\"form-control\" id=\"first_named_inventor\" name=\"first_named_inventor\">\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"art_unit\">Art Unit:</label>\n" +
    "              <input ng-disabled=\"loading_application_data\" ng-model=\"art_unit\" type=\"text\" class=\"form-control\" id=\"art_unit\" name=\"art_unit\">\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"examiner_name\">Examiner Name:</label>\n" +
    "              <input ng-disabled=\"loading_application_data\" ng-model=\"examiner_name\" type=\"text\" class=\"form-control\" id=\"examiner_name\" name=\"examiner_name\">\n" +
    "            </div>\n" +
    "\n" +
    "            <div class=\"form-group\">\n" +
    "              <label for=\"docket_number\">Attorney Docket Number:</label>\n" +
    "              <input ng-disabled=\"loading_application_data\" ng-model=\"attorney_docket_number\" type=\"text\" class=\"form-control\" id=\"docket_number\" name=\"docket_number\">\n" +
    "            </div>\n" +
    "        </div>\n" +
    "    </form>\n"
  );

}]);
