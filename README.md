Сервер для предоставления информации по географическим объектам. Предоставляет REST API сервис со следующими методами:

/api/get_by_id/<int:town_id>
Метод принимает численное значение id и по нему возвращает информацию о городе;
Если город не найден, то возвращается ошибка 404;

/api/towns_info/<town1>/<town2>
Метод принимает названия двух городов (на русском языке) и возвращает информацию о двух городах, 
дополнительно выводит какой из городов севернее, информацию о том, находятся ли города в разных временных зонах и разницу между временными зонами; 
Если какой-то из городов не был найден, то возвращается ошибка 404

/api/towns_clue/<town1>
Метод принимает часть названия города и возвращает все возможные варианты продолжений;
Eсли хотя бы один город не найден, то возвращается ошибка 404;

/towns_list/<int:page>/<int:number>'
Метод принимает численные значения страницы и число городов, отображаемых на странице, на основе этого отображает количество городов в указаном диапазоне на выбранной странице
Было принято, что максимальное количество городов, отображаемых на странице равно 100; 
Максимальное количество страниц, согласно текущему набору данных 3667; 
Максимальное количество страниц, которые можно отобразить на последней странице - 28; 
Если получено количество страниц/отображаемых городов, превышаемых максимм, то возвращается ошибка 404;