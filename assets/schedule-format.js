function isOdd(num) {
    return num % 2;
}

function lowerWeekHighlight() {
    if (isOdd(moment().week())) {
        $('.upper').addClass('faded');
    } else {
        $('.lower').addClass('faded');
    }
}

function highlightCurrentDayOfWeek(currentDayOfWeek) {
    var dayOfWeekClassList = ['.day_na', '.day_mon', '.day_tue', '.day_wed', '.day_thu', '.day_fri', '.day_sat'];
    $(dayOfWeekClassList[currentDayOfWeek]).addClass('highlighted');
}

function addDateToHeaderRow() {
    $('.day-of-week').each(function (index) {
        var dateMoment = moment().startOf('week').add(index + 1, 'days');
        var dateString = dateMoment.format('ddd') + '  ' + dateMoment.format('DD MMM');
        $(this).text(dateString);
    });
}

function setupEditableTable() {

    /* mindmup-editabletable.js */
    $('.table').editableTableWidget({
        editor: $('<textarea class="table-editor">'),
        cloneProperties: ['padding', 'padding-top', 'padding-bottom', 'padding-left', 'padding-right',
            'text-align', 'color', 'border-radius']
    });
    $('td').on('change', function (evt, newValue) {
        console.log(newValue);
        return false; // reject change
    });
}

$(function ($) {
    lowerWeekHighlight();
    addDateToHeaderRow();
    highlightCurrentDayOfWeek((new Date()).getDay());
    setupEditableTable();
});
