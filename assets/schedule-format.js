function isOdd(num) {
    return num % 2;
}

function setupClassForWeek() {
    if (isOdd(moment().week())) {
        $('.upper').addClass('faded');
    }
    else {
        $('.lower').addClass('faded');
    }
}

function highlightCurRow(currentDayOfWeek) {
    var dayOfWeekClassList = ['.day_na', '.day_mon', '.day_tue', '.day_wed', '.day_thu', '.day_fri', '.day_sat'];
    $(dayOfWeekClassList[currentDayOfWeek]).addClass('highlighted');
}

function setupHeaderRow() {
    $('.day-of-week').each(function (index) {
        var dateMoment = moment().startOf('week').add(index + 1, 'days');
        var dateString = dateMoment.format('ddd') + '  ' + dateMoment.format('DD MMM');
        $(this).text(dateString);
    });
}

$(function ($) {
    setupClassForWeek();
    setupHeaderRow();
    highlightCurRow((new Date()).getDay())
});
