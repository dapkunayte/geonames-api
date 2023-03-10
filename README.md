<h1> geonames api </h1>
<h3>  Сервер для предоставления информации по географическим объектам. Предоставляет REST API сервис со следующими методами: </h3>


<h4> /api/get_by_id/&ltint:town_id&gt </h4>
<ul>
<li> Метод принимает численное значение id и по нему возвращает информацию о городе; </li>
<li> Если город не найден, то возвращается ошибка <i>404</i>; </li>
</ul>

<h4> /api/towns_info/&lttown1&gt/&lttown2&gt </h4>
<ul>
<li> Метод принимает названия двух городов (на русском языке) и возвращает информацию о двух городах, 
дополнительно выводит какой из городов севернее, информацию о том, находятся ли города в разных временных зонах и разницу между временными зонами; </li>
<li> Если какой-то из городов не был найден, то возвращается ошибка <i>404</i> </li>
</ul>

<h4> /api/towns_clue/&lttown1&gt </h4>
<ul>
<li> Метод принимает часть названия города и возвращает все возможные варианты продолжений; </li>
<li> Eсли хотя бы один город не найден, то возвращается ошибка <i>404</i>; </li>
</ul>

<h4> /towns_list/&ltint:page&gt/&ltint:number&gt </h4>
<ul>
<li> Метод принимает численные значения страницы и число городов, отображаемых на странице, на основе этого отображает количество городов в указаном диапазоне на выбранной странице </li>
<li> Было принято, что максимальное количество городов, отображаемых на странице равно <strong>100</strong> </li>
<li> Максимальное количество страниц для используемого набора данных - <strong>3667</strong> </li>
<li> Максимальное количество страниц, которые можно отобразить на последней странице - <strong>28</strong> </li>
<li> Если получено количество страниц/отображаемых городов, превышаемых максимм, то возвращается ошибка <i>404</i> </li>
</ul>
