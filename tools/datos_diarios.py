#!/usr/bin/env python3
"""Contenido completo de los Diarios (Guía del Guardián, Dossier y Ayudas de juego) para El Simulacro desatado.
100 % fiel al PDF oficial sin datos inventados.
"""

MOD = "mr-simulacro-desatado"
R = lambda p: f"modules/{MOD}/assets/{p}"

def paginas_guia(uuids_actores, uuids_ayudas, uuids_escenas):
    A = lambda slug, label=None: f"@UUID[Actor.{uuids_actores[slug]}]{{{label or slug}}}"
    H = lambda slug, label: f"@UUID[JournalEntry.{uuids_ayudas[slug]}]{{{label}}}"
    S = lambda slug, label: f"@UUID[Scene.{uuids_escenas[slug]}]{{{label}}}"

    return [
        ("01 · Introducción y trasfondo", f"""
<h1>Estambul 2013 · El Simulacro desatado</h1>
<p><em>Por Mike Mason y Penelope Love · Epílogo contemporáneo de la campaña Horror en el Orient Express.</em></p>
<p>En el que los investigadores se enfrentan a misteriosos y horribles asesinatos, ecos letales del pasado, y a un plan demencial para crear un Simulacro contemporáneo.</p>

<blockquote>
<p><strong>Una secuela opcional:</strong> este escenario está diseñado para seis personajes jugadores (aunque funciona con grupos más pequeños) tras haber vivido la campaña de 1923. Al menos <strong>uno de los PJ debe ser descendiente</strong> de uno de los investigadores que participaron en los acontecimientos del tren en 1923. Toma nota de los momentos memorables de tu campaña original para evocarlos como «ecos del pasado» en el Otro Lado.</p>
</blockquote>

<h2>Información para los investigadores</h2>
<p><strong>Lux-Vista.com</strong> es una nueva empresa de internet fundada por el millonario inglés de 32 años {A('john-milton', 'John Milton')} que promete viajes de lujo para todos los bolsillos. Para su lanzamiento ha organizado el concurso <em>«Cualquiera puede viajar»</em>, regalando <strong>12 billetes gratuitos</strong> con todos los gastos pagados para el Orient Express actual. Cada investigador ha ganado uno de esos billetes y no conoce a los demás hasta llegar a Londres o a la estación <em>Gare de l’Est</em> de París.</p>
<p>Es fácil encontrar información pública sobre Milton en internet: entrega a los jugadores la {H('ayuda-1', 'Ayuda de juego · Actualidad 1 (Perfil: John Milton)')}.</p>

<h2>Información para el Guardián: el plan de John Milton</h2>
<p>Lo que el mundo ignora es que {A('john-milton', 'John Milton')} es un devoto adorador de <strong>Nyarlathotep</strong>. Mientras estudiaba Filología Clásica en Londres, buscó en la Biblioteca Británica el <em>«Pergamino de Sedefkar: Ritual de purificación»</em>. En su lugar halló un <strong>diario manuscrito de 1923</strong> escrito por uno de los investigadores originales de <em>Horror en el Orient Express</em>; un misterioso bibliotecario le sugirió además consultar la traducción inglesa del <em>Necronomicón</em> con anotaciones al margen sobre el Simulacro de Sedefkar, los Hermanos de la Piel y el Ritual de restauración.</p>
<p>Convencido de que necesita una gran obra para atraer la mirada de Nyarlathotep, Milton planea construir un <strong>«Simulacro de Carne»</strong> con las partes del cuerpo de seis víctimas reunidas mediante el concurso amañado de Lux-Vista:</p>
<ol>
  <li>Realizar una versión alterada del <strong>Ritual de purificación</strong> a bordo del tren para convocar y consumir el espíritu de Mehmet Makryat.</li>
  <li>Asesinar durante el viaje a cinco ganadores del concurso y, como sexta víctima final, al <strong>PJ descendiente de 1923</strong> (cuya cabeza coronará el Simulacro).</li>
  <li>Abrir un portal hasta la <strong>Mezquita Velada</strong> de Estambul (que compró en secreto), realizar el <strong>Ritual de restauración</strong> y lograr que los supervivientes le maten dentro del círculo de sangre para que su espíritu posea el {A('simulacro-de-carne', 'Simulacro de Carne')}.</li>
</ol>

<h2>Consecuencias inesperadas</h2>
<p>La versión alterada del <em>Ritual de purificación</em> que Milton ejecuta la noche del Día 3 sale mal: en lugar de convocar el alma de Makryat, abre una grieta en el espacio-tiempo que arrastra los <strong>cinco últimos vagones del Orient Express</strong> a una dimensión de bolsillo llamada <strong>el Otro Lado</strong>, donde los ecos del pasado de 1923 y de la historia del tren se vuelven físicos y mortales.</p>
"""),

        ("02 · El Orient Express en 2013", f"""
<h1>El tren actual y la vida a bordo</h1>
<p>Restaurado por James Sherwood desde 1977 y puesto de nuevo en servicio en 1982, el Orient Express contemporáneo recrea el esplendor de los Años 20. Una vez al año realiza el trayecto completo de París a Estambul durante seis días (11.000 £ / 11.800 € / 16.997 $ por persona en cabina doble), con paradas nocturnas en hoteles de lujo para compensar la ausencia de duchas.</p>
<p>Consulta los planos de los vagones de los investigadores: {S('coches-mesa', 'Coches cama F y G (Mesa)')} y {S('coches-guardian', 'Coches cama F y G (Guardián)')}.</p>

<h2>Composición del tren (14 coches)</h2>
<ul>
  <li>Locomotora y ténder · Furgón de equipaje · Dormitorios para el personal</li>
  <li>Coche restaurante: <em>Étoile du Nord</em> · Coches cama A, B y C</li>
  <li>Coche restaurante: <em>La Côte</em> · Coche cama D</li>
  <li><strong>Coche salón E</strong> <em>(trasladado al Otro Lado)</em></li>
  <li><strong>Coche restaurante: <em>La Saveur d’Asie</em></strong> <em>(trasladado al Otro Lado)</em></li>
  <li><strong>Coche cama F</strong> y <strong>Coche cama G</strong> <em>(trasladados al Otro Lado)</em></li>
  <li><strong>Furgón de equipaje trasero</strong> <em>(trasladado al Otro Lado)</em></li>
</ul>

<h2>Normas, comidas y logística</h2>
<ul>
  <li><strong>Comidas:</strong> desayuno (07:00–09:00) y té de la tarde en la cabina; comida y cena en los coches restaurante ({H('ayuda-2', 'Ayuda 2 · Menú de ejemplo')}). El coche bar cuenta con un piano de cuarto de cola.</li>
  <li><strong>Vestimenta:</strong> «Nunca vas demasiado arreglado en el Orient Express». Prohibidos vaqueros, pantalones cortos, camisetas y zapatillas. Etiqueta de noche o corbata negra para cenar.</li>
  <li><strong>Aseo y equipaje:</strong> lavabo con agua caliente (caldera de carbón por coche) y baño compartido al final del vagón. Una pieza de mano + portatrajes en cabina; la maleta facturada va en el furgón de equipaje (inaccesible en ruta).</li>
  <li><strong>Comunicaciones:</strong> sin wifi ni cobertura estable; en marcha solo se permite una tirada <strong>Extrema de Suerte</strong> en zonas pobladas, con cortes e interferencias. En el Otro Lado no hay señal alguna.</li>
  <li><strong>Idiomas y moneda:</strong> los azafatos hablan francés, inglés e italiano. Precios a bordo en euros.</li>
  <li><strong>Aduanas:</strong> en 2013 se requiere visado para Rumanía (gestionado por el personal) y Turquía (en frontera).</li>
</ul>

<h2>Equipo de emergencia a bordo</h2>
<p>Taladro · Kit de primeros auxilios en cada coche · Cincel de madera · Extintor en cada coche · Martillos ×2 · Sierra de metal · Hacha · Cuchilla · Sierras ×3 · Palas largas ×2 · Palancas ×3 · Aceite para engrasar · Palas ×2 · Mazo.</p>
"""),

        ("03 · Cronología y las seis víctimas", f"""
<h1>Las seis partes del cuerpo</h1>
<p>Milton marca discretamente con tiza roja el somier inferior de la cama de cada víctima el Día 3. Puede adaptar su lista si los PJ frustran un asesinato.</p>
<table>
  <thead><tr><th>Orden</th><th>Víctima prevista</th><th>Parte del cuerpo</th><th>Coche</th><th>Nicho (Mezquita)</th></tr></thead>
  <tbody>
    <tr><td>1.ª</td><td>{A('giuseppe-roti', 'Giuseppe Roti')}</td><td>Brazo izquierdo</td><td>Coche G</td><td>4.º nicho</td></tr>
    <tr><td>2.ª</td><td>{A('john-walters', 'John Walters')}</td><td>Brazo derecho</td><td>Coche G</td><td>2.º nicho</td></tr>
    <tr><td>3.ª</td><td>{A('enzo-banuelos', 'Enzo Bañuelos')}</td><td>Pierna izquierda</td><td>Coche F</td><td>6.º nicho</td></tr>
    <tr><td>4.ª</td><td>{A('oscar-griffin', 'Oscar Griffin')}</td><td>Pierna derecha</td><td>Coche F</td><td>5.º nicho</td></tr>
    <tr><td>5.ª</td><td>{A('faustino-gonzaga', 'Faustino Gonzaga')}</td><td>Torso</td><td>Coche F</td><td>3.º nicho</td></tr>
    <tr><td>6.ª</td><td><strong>PJ descendiente de 1923</strong> <em>(o {A('antonio-abella', 'Antonio Abella')})</em></td><td>Cabeza</td><td>Coche F</td><td>1.º nicho (última)</td></tr>
  </tbody>
</table>
<p><em>Reemplazo de PJ:</em> si un PJ muere, el jugador puede asumir el papel de {A('antonio-abella', 'Antonio Abella')}, {A('lars-farber', 'Lars Färber')}, {A('wanda-zeigler', 'Wanda Zeigler')}, {A('marisa-ocana', 'Marisa Ocaña')}, {A('chantel-antin', 'Chantel Antin')}, {A('henri-guillemette', 'Henri Guillemette')} o {A('mark-wilson', 'Mark Wilson')}.</p>

<h2>Resumen de la cronología (5 días)</h2>
<ul>
  <li><strong>Día 1 (viernes 30 de agosto):</strong> embarque en París Gare de l’Est (15:53), recepción de Lux-Vista (16:30) y cena de gala (19:00–22:00).</li>
  <li><strong>Día 2 (sábado 31 de agosto):</strong> incidente de {A('faustino-gonzaga', 'Faustino Gonzaga')} en la comida; llegada a Budapest (15:42) y alojamiento en el hotel Hilton; crisis de {A('chantel-antin', 'Chantel Antin')} en la cena por una nueva carta anónima; altercado entre {A('giuseppe-roti', 'Roti')} y {A('antonio-abella', 'Abella')}.</li>
  <li><strong>Día 3 (domingo 1 de septiembre):</strong> tour por Budapest y petición de auxilio de Chantel en el Laberinto de Buda; Milton vuelve al tren, roba la llave maestra con <em>Dominar</em>, marca las camas con tiza y roba 4 camisas a dos PJ; salida hacia Rumanía (18:08); Milton ejecuta el <em>Ritual de purificación</em>, la mitad trasera pasa al <strong>Otro Lado</strong> y asesina de madrugada a Roti y Walters.</li>
  <li><strong>Día 4 (lunes 2 de septiembre):</strong> descubrimiento del tren partido y de los cuerpos de Roti y Walters; informe del Dr. {A('fabian-wyss', 'Fabian Wyss')}; asesinatos de Bañuelos, Griffin y Gonzaga; aparece el <strong>diario de 1923</strong> junto al 5.º cadáver; enfrentamiento entre {A('mark-wilson', 'Mark Wilson')} y Chantel Antin; posible registro de cabinas.</li>
  <li><strong>Día 5 (martes 3 de septiembre):</strong> 6.º asesinato (Abella o PJ descendiente); Milton abre el portal en el túnel protegido por seis {A('soldado-sin-rostro', 'Soldados sin rostro')}; enfrentamiento final en la {S('mezquita', 'Mezquita Velada')} de Estambul.</li>
</ul>
"""),

        ("04 · Día 1: Viernes 30 de agosto (París)", f"""
<h1>Día 1 · Viernes 30 de agosto</h1>
<p><strong>Escena recomendada:</strong> {S('portada', 'Portada · Horror en el Orient Express')} · <strong>Música:</strong> <em>Escena 1 · Embarque en París</em> + <em>Sonido del Orient Express</em>.</p>
<ul>
  <li><strong>15:53</strong> — Subida al Orient Express en París <em>Gare de l’Est</em>.</li>
  <li><strong>16:30</strong> — Recepción de bienvenida de Lux-Vista en el coche salón E.</li>
  <li><strong>19:00–22:00</strong> — Cena en los coches restaurante.</li>
</ul>

<h2>¡Todos a bordo!</h2>
<p>Los investigadores ocupan cabinas en el <strong>Coche cama F</strong> (consulta {S('coches-guardian', 'Plano del Guardián')}). En cada compartimento hallan jabón, cepillos, batas, zapatillas, paraguas y posavasos con el logotipo del OE, bombones y un sobre elegante de Lux-Vista invitándoles a las 16:30 al coche salón. Entrega la {H('ayuda-3', 'Ayuda 3 · Itinerario del Orient Express')}.</p>
<p>El azafato {A('rene-violet', 'René Violet')} (coche F) o Jacques Côte (coche G) llama a la puerta, se presenta y avisa de que el té se servirá en el coche salón.</p>

<h2>Recepción de bienvenida y cena</h2>
<p>{A('john-milton', 'John Milton')} ejerce de anfitrión impecable con champán y presenta a los doce ganadores:</p>
<ul>
  <li>{A('antonio-abella', 'Antonio Abella')}: callado y reticente, mueve los dedos con nerviosismo.</li>
  <li>{A('oscar-griffin', 'Oscar Griffin')}: encantado de hacer amigos y charlar sin parar.</li>
  <li>{A('faustino-gonzaga', 'Faustino Gonzaga')}: habla casi todo el tiempo de comida.</li>
  <li>{A('giuseppe-roti', 'Giuseppe Roti')}: distante, evalúa en silencio al resto.</li>
  <li>{A('john-walters', 'John Walters')}: abrumado por el lujo, conversación forzada.</li>
  <li>{A('enzo-banuelos', 'Enzo Bañuelos')}: deslumbrado como un ciervo ante unos faros; se pegará a quien hable español o italiano.</li>
</ul>
<p>A las 18:00 Milton anuncia la cena (recomienda la ternera; muestra la {H('ayuda-2', 'Ayuda 2 · Menú de ejemplo')}). El maître exige etiqueta estricta. Hacia las 23:00 el coche bar cierra y el azafato pregunta la hora del desayuno.</p>
"""),

        ("05 · Día 2: Sábado 31 de agosto (Budapest)", f"""
<h1>Día 2 · Sábado 31 de agosto</h1>
<p><strong>Escena recomendada:</strong> {S('budapest', 'Budapest · El Danubio y el Parlamento')} · <strong>Música:</strong> <em>Escena 2 · Budapest y el Laberinto</em>.</p>
<ul>
  <li><strong>07:00–09:00</strong> — Desayuno en los compartimentos.</li>
  <li><strong>12:00–14:00</strong> — Comida en los vagones restaurante.</li>
  <li><strong>15:42</strong> — Llegada a la estación oeste de Budapest (<em>Nyugati Pályaudvar</em>) y traslado al <strong>Hotel Hilton</strong> (16:30).</li>
  <li><strong>19:00–22:00</strong> — Cena en el restaurante <em>Icon</em> del hotel.</li>
</ul>

<h2>¿Quién ha cocinado esto? (Comida en La Côte)</h2>
<p>{A('faustino-gonzaga', 'Faustino Gonzaga')}, bebido e indignado por el salmón, intenta irrumpir en la cocina. Si un PJ interviene y supera una tirada de <strong>Encanto, Intimidar o Persuasión</strong>, Gonzaga se calma y se disculpa avergonzado al aparecer el chef. Si falla dos veces, lanza un puñetazo torpe (evitable salvo pifia en <strong>Esquivar</strong>) y los azafatos lo escoltan a su cabina.</p>

<h2>Noche en el Hotel Hilton de Buda</h2>
<p>Situado junto a la iglesia de Matías y el Bastión de los Pescadores, con vistas al Danubio y al Parlamento, gimnasio 24 h y wifi ilimitado.</p>
<ul>
  <li><strong>Crisis de Chantel Antin:</strong> durante la cena parece angustiada mientras {A('henri-guillemette', 'Henri Guillemette')} se muestra indiferente (tirada de <strong>Psicología</strong>). Antes de cenar descubrió otra carta del acosador en su bolso. Sale corriendo a su habitación; si un PJ llama a la puerta, solo abrirá a Guillemette. Con <strong>Escuchar</strong> la oyen sollozar; si fallan, grita: <em>«¡Váyase! ¡Le oigo! Déjeme sola y deje de enviarme cartas»</em>.</li>
  <li><strong>Sospecha sobre Antonio Abella:</strong> tras la cena, {A('giuseppe-roti', 'Giuseppe Roti')} invita a {A('antonio-abella', 'Antonio Abella')} a pasear por los jardines, pero este se niega alegando cansancio. Con <strong>Psicología</strong> se nota que miente: teme encontrarse con la policía. Se encerrará en su cuarto hasta volver al tren en taxi el Día 3.</li>
</ul>
"""),

        ("06 · Día 3: Domingo 1 de septiembre (El Ritual)", f"""
<h1>Día 3 · Domingo 1 de septiembre</h1>
<ul>
  <li><strong>10:00–16:00</strong> — Tour guiado opcional por Budapest (ni Abella ni Milton asisten).</li>
  <li><strong>16:30</strong> — Té de la tarde en las cabinas · <strong>18:08</strong> — Salida del OE hacia Rumanía · <strong>19:00–22:00</strong> — Cena.</li>
</ul>

<h2>El tour por Budapest y el Laberinto de Buda</h2>
<p>Recorre la plaza de la Santísima Trinidad, la iglesia de Matías, la casa de los vinos húngaros, el distrito del Castillo de Buda y concluye en el <strong>Laberinto del Castillo de Buda</strong> (a 16 m de profundidad, con figuras de cera y la escalofriante <em>cabeza coronada</em>).</p>
<figure><img src="{R('diario/laberinto-buda.webp')}" alt="La cabeza coronada en el Laberinto de Buda" style="max-width:100%;border-radius:4px;" /><figcaption><em>La cabeza coronada en el Laberinto del Castillo de Buda.</em></figcaption></figure>

<h2>Una petición de auxilio</h2>
<p>En una cámara apartada del laberinto, {A('chantel-antin', 'Chantel Antin')} se escabulle de Guillemette, da un suave codazo a un PJ y susurra: <em>«Por favor, venga conmigo, necesito su ayuda»</em>. Confiesa que lleva seis meses acosada por «El amor de TU vida», que cree que viaja en el tren y le muestra la {H('ayuda-4', 'Ayuda 4 · Carta anónima con recortes')}. No menciona su derringer oculta. <strong>Psicología</strong> confirma su sinceridad.</p>
<p><strong>Ojo con Mark Wilson:</strong> tiene <strong>Descubrir 30 %</strong> y <strong>Sigilo 70 %</strong>. Si los ve apartarse, escucha la conversación y desarrolla celos mortales contra ese PJ (además de Guillemette).</p>

<h2>El asesino se prepara (en el tren)</h2>
<p>Mientras todos están en el tour, {A('john-milton', 'John Milton')} regresa al tren, usa <strong>Dominar</strong> sobre un azafato para conseguir la <strong>llave maestra</strong> y borra su recuerdo. Entra en las cabinas de sus seis víctimas y dibuja con tiza roja bajo el somier la parte del cuerpo asignada (incluida una <strong>cabeza</strong> bajo la cama del PJ descendiente — solo visible mirando expresamente bajo el somier con una tirada <strong>Extrema de Descubrir</strong>). También roba <strong>cuatro camisas</strong> (dos a cada uno de dos PJ) para usarlas durante los asesinatos. Finge estar indispuesto para saltarse la cena.</p>

<h2>El ritual sale mal (Madrugada)</h2>
<p>Mientras el tren cruza hacia Rumanía, Milton realiza su versión alterada del <em>Ritual de purificación</em>. El hechizo rasga el espacio-tiempo y traslada los <strong>cinco vagones traseros</strong> al <strong>Otro Lado</strong>. Los azafatos despiertos caen inconscientes; todos sufren pesadillas atroces con criaturas sin rostro. Enloquecido de euforia al creer que Nyarlathotep le sonríe, Milton se viste con una camisa robada y asesina esa misma noche a {A('giuseppe-roti', 'Giuseppe Roti')} (brazo izquierdo) y a {A('john-walters', 'John Walters')} (brazo derecho), guarda los brazos en una maleta en el furgón y arroja la camisa ensangrentada por una ventanilla del coche G.</p>
"""),

        ("07 · El Otro Lado y Ecos del Pasado", f"""
<h1>El Otro Lado</h1>
<p><strong>Música recomendada:</strong> <em>Escena 3 · El Otro Lado</em> + <em>Ambiente detectivesco lovecraftiano</em>.</p>
<p>Los cinco coches atrapados son: <strong>Coche salón E</strong>, <strong>La Saveur d’Asie</strong>, <strong>Coche cama F</strong>, <strong>Coche cama G</strong> y <strong>Furgón de equipaje</strong>. Solo quedan tres empleados a bordo: {A('rene-violet', 'René Violet')}, Jacques Côte y Didier Lagoy. Darse cuenta de que están atrapados cuesta <strong>1/1D4 COR</strong>.</p>
<ul>
  <li><strong>Mitos de Cthulhu:</strong> revela que han sido trasladados a una dimensión de bolsillo. Una segunda tirada sugiere que un <strong>portal</strong> es la única salida.</li>
  <li><strong>Ciencias ocultas:</strong> evoca los mitos feéricos donde el tiempo discurre de otro modo.</li>
</ul>

<h2>Ecos del pasado (1D6 minutos, físicos y letales)</h2>
<p>Usa la tabla aleatoria de <em>Ecos del Otro Lado</em> o recuerdos de tu campaña de 1923 (Fenalik, un PJ de 1923 durmiendo en su cama, piezas originales del Simulacro, camisas negras sin rostro, el Príncipe Rompecabezas, reptadores de carne, la bestia locomotora) y ecos históricos del Orient Express (bandidos de Anasthatos 1891, ventisca de 1929, Baden-Powell espía, Paul Deschanel en pijama 1920, vagón del armisticio 1918/1940).</p>

<h2>Encuentros en el Otro Lado</h2>
<ul>
  <li><strong>Mirar por la ventana:</strong> un rostro pálido de ojos lechosos aparece pegado al cristal entre la niebla (<strong>1/1D4 COR</strong>).</li>
  <li><strong>Salir por el terraplén al pinar:</strong> silencio absoluto, niebla helada y {A('soldado-sin-rostro', 'Soldados sin rostro')} inmóviles entre los pinos (<strong>1/1D6 COR</strong>). Disparan para herir y devolver a los pasajeros al tren. Al final del bosque una <strong>barrera invisible</strong> repele cualquier intento de cruzarla (<strong>Saltar o DES</strong> o sufrir 1D4 PV).</li>
  <li><strong>Seguir las vías:</strong> conduce a un túnel donde cualquier luz solo ilumina 60 cm; se oyen sollozos y respiraciones (<strong>0/1 COR</strong>) hasta topar con un <strong>muro de ladrillo indestructible</strong> antes de que lleguen los soldados sin rostro.</li>
  <li><strong>Grifos y bebidas:</strong> brota sangre estancada del lavabo o flota un globo ocular en una copa del coche salón (<strong>1/1D4 COR</strong>).</li>
  <li><strong>Furgón de equipaje:</strong> hedor rancio; al abrir una maleta aparece un cuerpo humano o una mano disecada ajena a Milton (<strong>1/1D4 COR</strong>).</li>
  <li><strong>El llanto de una niña:</strong> llora de espaldas al final del vagón; al tocarle el hombro se gira sin rostro (<strong>1/1D4 COR</strong>).</li>
</ul>
"""),

        ("08 · Día 4: Lunes 2 de septiembre (Asesinatos)", f"""
<h1>Día 4 · Lunes 2 de septiembre</h1>
<p><strong>Planos:</strong> {S('coches-mesa', 'Coches cama F y G (Mesa)')} · {S('coches-guardian', 'Coches cama F y G (Guardián)')}.</p>

<h2>El tren desaparecido y los primeros cadáveres</h2>
<p>El tren está detenido. {A('rene-violet', 'René Violet')} descubre horrorizado que todos los coches delanteros han desaparecido: los conectores parecen cortados por un cuchillo gigante. Nadie tiene señal.</p>
<ul>
  <li><strong>Cabina de Giuseppe Roti (Coche G):</strong> cuello rajado en la cama, sin el brazo izquierdo (<strong>1/1D3 COR</strong>). Ventanilla abierta.</li>
  <li><strong>Cabina de John Walters (Coche G):</strong> sangre en paredes y suelo, once puñaladas, sin el brazo derecho (<strong>1/1D4 COR</strong>). Ventanilla abierta.</li>
  <li><strong>Informe del Dr. {A('fabian-wyss', 'Fabian Wyss')}:</strong> amputaciones <em>post mortem</em> entre las 02:00 y 06:00, asesino diestro, probablemente conocido de las víctimas y delgado o bajo si salió por la ventanilla.</li>
  <li><strong>Marcas de tiza:</strong> una tirada de <strong>Descubrir</strong> en cualquiera de las cabinas revela los dibujos con tiza roja bajo la cama (forzar y fallar borra el dibujo).</li>
  <li><strong>Camisa ensangrentada:</strong> <strong>Descubrir</strong> junto al exterior derecho del coche G halla una de las camisas robadas a los PJ.</li>
</ul>

<h2>Asesinatos 3, 4 y 5 + Una pista crucial</h2>
<p>Aprovechando el caos, Milton asesina sucesivamente a {A('enzo-banuelos', 'Enzo Bañuelos')} (pierna izquierda), {A('oscar-griffin', 'Oscar Griffin')} (pierna derecha) y {A('faustino-gonzaga', 'Faustino Gonzaga')} (torso). Junto al 5.º cadáver deja el <strong>diario de 1923</strong> (propiedad del Museo Británico) con el relato de los Hermanos de la Piel y las dos versiones del <em>Ritual de purificación</em> (la primera marcada como «versión imprecisa»).</p>

<h2>Mark Wilson habla con Chantel Antin</h2>
<p>{A('mark-wilson', 'Mark Wilson')} desliza la {H('ayuda-5', 'Ayuda 5 · Nota manuscrita para Chantel')} bajo su puerta. Al acudir a la cita (posiblemente con un PJ oculto), Wilson se declara; al ser rechazado saca su cuchillo y Chantel le dispara a quemarropa con su derringer (6 PV). Si huye al bosque puede ser atrapado, regresar a por Chantel o convertirse en víctima de Milton.</p>

<h2>Registro de cabinas y el diario de Milton</h2>
<p>Registrar cabinas exige <strong>Persuasión, Encanto o Intimidar</strong> y presencia de un azafato. Milton intentará plantar su navaja en otra cabina con <em>Dominar</em> o huir al bosque. Si registran su cabina antes de que la limpie hallarán:</p>
<ul>
  <li><strong>El diario de John Milton</strong> ({H('ayuda-6', 'Ayuda 6 · Fragmentos 1, 2 y 3')}): 1D6+2 h de lectura, <strong>1D6 COR</strong>, <strong>+3 % Mitos de Cthulhu</strong>; contiene el <em>Ritual de purificación</em>, el <em>Ritual de restauración</em> (donde revela que debe morir para activar el Simulacro) y <em>Crear portal</em>.</li>
  <li><strong>Las camisas robadas</strong> (reconocibles con <strong>Descubrir</strong> por sus dueños).</li>
  <li><strong>Ingredientes rituales:</strong> bol de cobre grabado (<em>Mitos de Cthulhu</em>), hierbas pestilentes y tiza roja gastada.</li>
</ul>
<p><em>Si capturan a Milton:</em> deja de resistirse y negocia — afirma que solo él sabe abrir un portal para sacarlos del Otro Lado y exige sacrificar a tantas personas como partes le falten.</p>
"""),

        ("09 · Día 5 y Clímax: La Mezquita Velada", f"""
<h1>Día 5 · Martes 3 de septiembre y Clímax</h1>
<p><strong>Escenas:</strong> {S('estambul-mesa', 'Estambul (Mesa)')} · {S('estambul-guardian', 'Estambul (Guardián)')} · {S('mezquita', 'La Mezquita Velada')} · <strong>Música:</strong> <em>Escena 4 · La Mezquita Velada</em>.</p>

<h2>La sexta víctima y el portal</h2>
<p>Milton intenta aislar al PJ descendiente (o a {A('antonio-abella', 'Antonio Abella')} si prefieres no matar a un PJ) con un pretexto como haber visto un helicóptero fuera del tren. Hallar un cadáver decapitado cuesta <strong>1/1D4+1 COR</strong>.</p>
<p>Con las seis partes, Milton camina hacia el túnel de las vías y dedica <strong>1 hora</strong> a lanzar <em>Crear portal</em>, protegido por <strong>seis {A('soldado-sin-rostro', 'Soldados sin rostro')}</strong>. Al terminarlo grita: <em>«¡Venid a ver! ¡Seguidme! ¡Nos espera el nuevo amanecer!»</em> y salta al portal. Quien lo cruce pierde <strong>2 puntos de magia</strong> y aparece a las <strong>03:00</strong> en la sala principal de la Mezquita Velada. El portal permanece abierto <strong>1D4 horas</strong>.</p>
<blockquote><p><strong>Alternativa:</strong> si los PJ tienen el diario de Milton, pueden aprender <em>Crear portal</em> tras <strong>1D6+2 horas</strong> y una tirada <strong>Difícil de INT</strong>.</p></blockquote>

<h2>Enfrentamiento en la Mezquita Velada</h2>
<p>Clausurada desde finales de los años 20 y comprada por Milton con la excusa de hacer un hotel de lujo, la mezquita está iluminada solo por antorchas. Bajo la gran cúpula se alza una columna con seis nichos ocupados por las partes (la cabeza frente a ellos: <strong>1/1D4+1 COR</strong> si no sabían quién era la 6.ª víctima).</p>
<p>Milton espera sangrando en el centro de un círculo de sangre, arroja su cuchillo y grita: <em>«Ante vosotros… ¡mi obra! ¡Me entrego a vuestra justicia! Proceded como yo para tener vuestra venganza.»</em></p>
<ul>
  <li>Si nadie lo mata, usa <strong>Dominar</strong> sobre un PJ para que lo haga; como último recurso se degüella él mismo (<strong>0/1 COR</strong>).</li>
  <li><strong>Impedir el suicidio:</strong> frustra por completo el plan; Milton acaba llorando en una celda turca.</li>
  <li><strong>Si Milton muere:</strong> las seis partes flotan hacia el círculo para unirse en el {A('simulacro-de-carne', 'Simulacro de Carne')} (<strong>1/1D6 COR</strong>). Un PJ rápido puede atrapar una parte con <strong>Combatir</strong> (o <strong>DES</strong>) y destruirla para arruinar el ritual.</li>
  <li><strong>Combate contra el Simulacro:</strong> si sus PV bajan a la mitad (≤ 8 PV), intentará huir en la noche de Estambul.</li>
</ul>

<h2>Conclusión y recompensas de Cordura</h2>
<p>Los supervivientes salen a Estambul antes del amanecer mientras suena la llamada al rezo del <em>Fajr</em>. Las autoridades demuelen finalmente la Mezquita Velada.</p>
<ul>
  <li><strong>+1D6 COR</strong> — Evitar que Milton cometa los seis asesinatos.</li>
  <li><strong>+1D6 COR</strong> — Evitar que Milton se suicide y complete el Ritual de restauración.</li>
  <li><strong>+1D4 COR</strong> — Evitar que las partes del cuerpo se unan para formar el Simulacro de Carne.</li>
  <li><strong>+1D4 COR</strong> — Capturar a Milton y entregarlo a las autoridades.</li>
  <li><strong>+1D6 COR</strong> — Destruir el Simulacro de Carne activado.</li>
  <li><strong>+1D4 COR</strong> — Salvar a Chantel Antin de su acosador, Mark Wilson.</li>
  <li><strong>+1D4 COR</strong> — Descubrir a Angelo Minotti (Antonio Abella) y entregarlo a las autoridades.</li>
</ul>
"""),

        ("10 · Notas de uso del módulo MR-", f"""
<h1>Cómo dirigir con MR- El Simulacro Desatado</h1>
<p>Este módulo prepara la aventura completa para <strong>Call of Cthulhu 7th Edition (CoC7)</strong> en Foundry VTT v13/v14 siguiendo las convenciones de la serie <code>MR-</code>:</p>
<ul>
  <li><strong>Panel del Guardián:</strong> ábrelo desde el botón del tren (<i class="fa-solid fa-train"></i>) en la barra izquierda o mediante la macro de la barra rápida. Permite llevar el <strong>día actual</strong>, alternar entre <em>Mundo real / El Otro Lado / Mezquita Velada</em>, tachar las <strong>6 partes del Simulacro de Carne</strong>, mostrar cualquier <strong>Ayuda de juego</strong> a los jugadores en un clic, lanzar <strong>Ecos del Otro Lado</strong> y otorgar las <strong>recompensas de Cordura</strong>.</li>
  <li><strong>Escenas dobles (Mesa y Guardián):</strong> tanto los <em>Coches cama F y G</em> como el mapa de <em>Estambul</em> incluyen versión limpia para los jugadores y versión anotada exclusiva para el Guardián. La <em>Mezquita Velada</em> trae muros y antorchas configuradas.</li>
  <li><strong>Integración con MR- Dirección:</strong> si tienes activo <em>MR- Dirección</em>, el módulo registra automáticamente el paquete de dirección con escenas, motivos musicales e hitos narrativos.</li>
  <li><strong>Integración con MR- Pizarra:</strong> desde el Panel del Guardián o la macro dedicada puedes importar la <strong>Pizarra de investigación del Orient Express</strong> con cinco capas revelables progresivamente.</li>
</ul>
"""),
    ]


AYUDAS_DEF = [
    {
        "slug": "ayuda-1",
        "name": "Ayuda 1 · Perfil: John Milton",
        "pages": [
            ("Perfil web: John Milton", f"""
<p><img src="{R('ayudas/actualidad-1-milton.webp')}" alt="Perfil: John Milton" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<h2>orientexpresswriters.wordpress.com / John Milton</h2>
<p>A los 20 años, John Milton creó <em>red-heart.com</em>, una página web de citas online que surgió de la nada y se convirtió en una de las más famosas casi de la noche a la mañana. En tres años, Milton había vendido la web por 2,5 millones de dólares. Ha seguido encontrando y vendiendo numerosas webs conocidas basadas en negocios entre las que se incluyen <em>grappy.com</em>, centrada en la moda; el vendedor de música <em>bombilate.com</em> y <em>ogee.com</em>, la proveedora de comida de lujo.</p>
<p>Nacido en 1981, los humildes orígenes de Milton se documentan en su autobiografía de 2010, <em>Más allá de la colina</em>. Hijo único de unos padres de clase media, se formó en la escuela secundaria Bakewell, en Derbyshire (Inglaterra), antes de marcharse a estudiar Filología Clásica en la Universidad de Londres. Milton dejó los estudios, alegando que quería enfocarse en su nuevo negocio de internet (<em>red-heart.com</em>) y el resto es historia.</p>
<p>A partir de 2013, Milton lanza una nueva empresa, <em>lux-vista.com</em>, cuyo objetivo es ofrecer viajes de lujo asequibles para las masas. Esta nueva web ha llamado la atención de los inversores y de la prensa con la campaña de marketing de Milton «Cualquiera puede viajar», que ofrece 12 billetes gratuitos para el Orient Express, con todos los gastos pagados.</p>
""")
        ],
    },
    {
        "slug": "ayuda-2",
        "name": "Ayuda 2 · Menú de ejemplo (La Carte)",
        "pages": [
            ("La Carte · Orient Express", f"""
<p><img src="{R('ayudas/actualidad-2-menu.webp')}" alt="Menú de ejemplo La Carte" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<h3>Pour Démarrer</h3>
<ul>
  <li><strong>Rainbow Chou-Fleur Soupe</strong> (sopa de coliflor, caviar de salmón)</li>
  <li><strong>Duck œuf et les Asperges</strong> (espárragos, pesto de habas y huevo de pato)</li>
</ul>
<h3>Plat de Résistance</h3>
<ul>
  <li><strong>Fromage de Chèvre et Champ Tarte aux Champignons</strong> (queso de cabra y pastel de champiñones)</li>
  <li><strong>Aubaine Filet de Bœuf avec Pommes de Terre Nouvelles et Salade</strong> (filete de ternera Aubaine con patatas tempranas y ensalada)</li>
  <li><strong>Le Homard Spaghetti</strong> (espaguetis, bogavante, tomate y albahaca)</li>
  <li><strong>Salade du Marché</strong> (ensalada de temporada con lechugas variadas, rábanos, tomate y olivas)</li>
</ul>
<h3>À Suivre</h3>
<ul>
  <li><strong>La Sélection du Maître Fromager</strong> (selección de quesos)</li>
  <li><strong>Salade de fruits frais</strong> (ensalada de fruta fresca)</li>
  <li><strong>Composition Framboises/Amandes</strong> (arreglo de frambuesas y almendras)</li>
  <li><strong>Figues de Solliès Pochées</strong> (higos de Solliès escalfados)</li>
</ul>
""")
        ],
    },
    {
        "slug": "ayuda-3",
        "name": "Ayuda 3 · Itinerario del Orient Express",
        "pages": [
            ("Itinerario del Orient Express", f"""
<p><img src="{R('ayudas/actualidad-3-itinerario.webp')}" alt="Itinerario del Orient Express" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<table>
  <tbody>
    <tr><td><strong>Día 1 · Viernes 30 de agosto</strong></td><td>15:53 — Subida al OE en París Gare de l’Est.</td></tr>
    <tr><td><strong>Día 2 · Sábado 31 de agosto</strong></td><td>15:42 — El OE llega a Budapest, Hungría. Transporte hasta el hotel Hilton para pasar la noche.</td></tr>
    <tr><td><strong>Día 3 · Domingo 1 de septiembre</strong></td><td>10:00–16:00 — Tour guiado opcional por Budapest.<br/>18:08 — El OE sale hacia Rumanía.</td></tr>
    <tr><td><strong>Día 4 · Lunes 2 de septiembre</strong></td><td>08:52 — Llegada a Sinaia.<br/>10:00–12:00 — Visita guiada opcional al castillo de Peles.<br/>12:20 — Salida hacia Bucarest.<br/>14:16 — Llegada al norte de Bucarest, transporte al Athenee Palace Hilton Hotel.</td></tr>
    <tr><td><strong>Día 5 · Martes 3 de septiembre</strong></td><td>09:05 — Salida hacia Bulgaria.<br/>14:00–16:00 — Breve excursión en tren a Varna.<br/>17:04 — Salida hacia Turquía.</td></tr>
    <tr><td><strong>Día 6 · Martes 4 de septiembre</strong></td><td>15:18 — Llegada a la estación de Sirkeci en Estambul.</td></tr>
  </tbody>
</table>
""")
        ],
    },
    {
        "slug": "ayuda-4",
        "name": "Ayuda 4 · Carta anónima con recortes",
        "pages": [
            ("Carta del acosador de Chantel", f"""
<p><img src="{R('ayudas/actualidad-4-carta-recortes.webp')}" alt="Carta con recortes para Chantel" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<blockquote>
<p>ADORABLE CHANTEL</p>
<p>ME SACA DE MIS CASILLAS QUE SIGAS IGNORANDO MIS SÚPLICAS DE AMOR.<br/>
TIENES QUE OFRECERME ALGO.<br/>
TE DARÉ UNA ÚLTIMA OPORTUNIDAD.<br/>
PRONTO ME PONDRÉ EN CONTACTO CONTIGO.</p>
<p style="text-align:right;"><em>EL AMOR DE TU VIDA</em></p>
</blockquote>
""")
        ],
    },
    {
        "slug": "ayuda-5",
        "name": "Ayuda 5 · Nota manuscrita para Chantel",
        "pages": [
            ("Nota de cita para Chantel", f"""
<p><img src="{R('ayudas/actualidad-5-nota-cita.webp')}" alt="Nota manuscrita para Chantel" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<blockquote>
<p>Queridísima Chantel.</p>
<p>Reúnete conmigo hoy a las (——) pm en (——).<br/>
Ven sola.<br/>
Por favor, disculpa la necesidad de discreción.<br/>
Prometo que se descubrirá todo.</p>
</blockquote>
""")
        ],
    },
    {
        "slug": "ayuda-6",
        "name": "Ayuda 6 · Diario de John Milton",
        "pages": [
            ("Fragmento 1 · El Simulacro reencarnado", f"""
<p><img src="{R('ayudas/actualidad-6-fragmento-1.webp')}" alt="Diario de Milton - Fragmento 1" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<blockquote>
<p>Ningún hombre puede detenerme. Estoy listo. Cuento con el aklo y he preparado los componentes necesarios. ¡Tanto tiempo! Tanto tiempo he esperado, reuniendo los recursos. Sí, el SEÑOR OSCURO me encontrará sin quererlo. Nunca pararé, nunca se arrepentirá de haber depositado su confianza en mí, porque solo yo merezco crear el nuevo recipiente. Reunir las piezas y crear sangre nueva de otra sangre. Mi entusiasmo crece cada día, pero debo contenerme. Tengo que trabajar en silencio, en secreto, en las sombras hasta que mis peones estén en el tablero. Yo soy su amo, qué ignorantes son. Soy el pastor que lleva al rebaño al matadero. Creen que soy rico y poderoso, pero ahora eso son insignificancias. Les enseñaré lo que es de verdad el poder cuando mi cuchillo les haya cortado la carne y haya creado lo que solo yo puedo producir. ¡Iä! ¡Iä! ¡Nyarlathotep! ¡Señor de la piel! ¡Mi salvador! Cuando les haya cortado las partes correspondientes a esos idiotas, la sangre correrá, pero nadie sabrá lo que planeo. He bebido mucho de la sabiduría antigua y ahora es mi momento. Mi momento para hacer temblar al mundo en SU NOMBRE y ÉL me conocerá. Conocerá a su VERDADERO SIRVIENTE.</p>
<p><strong>¡El Simulacro reencarnado! ¡Yo soy el Simulacro!</strong></p>
</blockquote>
"""),
            ("Fragmento 2 · El descendiente", f"""
<p><img src="{R('ayudas/actualidad-6-fragmento-2.webp')}" alt="Diario de Milton - Fragmento 2" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<blockquote>
<p>Ya está hecho, por fin. Ningún linaje está oculto para mí. Richmond encontró la información del árbol genealógico de ese metomentodo, como describía mi visión. He enviado un billete al indigno descendiente. ¡No sospechan nada! Creerán que son afortunados cuando en realidad yo soy el dueño de su suerte. Paladearé la agitación de su muerte y respiraré hondo. Los miraré a los ojos mientras la sangre brota de los cortes que le haga. Les susurraré que LO SÉ. Que sé quiénes son y quién era el entrometido de su abuelo y que van a perder la vida por su AMO. Yo soy la mano de la venganza y liquidaré a quienes se opongan a ÉL, utilizando sus cuerpos como herramienta para mi creación más grandiosa. ¡Qué maravillosa ironía!</p>
</blockquote>
"""),
            ("Fragmento 3 · Los seis nichos y la ceremonia", f"""
<p><img src="{R('ayudas/actualidad-6-fragmento-3.webp')}" alt="Diario de Milton - Fragmento 3" style="max-width:100%;border-radius:4px;" /></p>
<hr/>
<blockquote>
<p>Hay que colocar los seis elementos en los nichos. El orden es preciso, como señalaba mi visión. El brazo derecho en el segundo, el izquierdo en el cuarto, el torso en el tercero, la pierna derecha en el quinto y la pierna izquierda en el sexto. La cabeza debe ser la última y se coloca en el primero. Walters, Roti, Gonzaga, Griffin, Bañuelos y, finalmente, el descendiente. ¡Iä! Este sirviente es listo. La ceremonia está preparada. Tengo los cantos del Ídolo. ÉL otorgará grandes maravillas a su sirviente, debo estar preparado. Tengo que ser digno de ello para que no me considere falso. ¡Nunca! Cortaré los elementos con mis propias manos en SU nombre y SABRÁ QUIÉN SOY. Ordenaré al resto que me liberen de mi cuerpo físico actual. Acabarán con John Milton de una cuchillada y mi esencia viajará al nuevo Simulacro, donde viviré y todo el poder será MÍO.</p>
</blockquote>
"""),
            ("Vista completa (3 fragmentos)", f"""
<p><img src="{R('ayudas/actualidad-6-diario-completo.webp')}" alt="Diario de Milton completo" style="max-width:100%;border-radius:4px;" /></p>
"""),
        ],
    },
]

ECOS_OTRO_LADO = [
    "Un PJ abre la puerta de su cabina y encuentra a un investigador de la campaña de 1923 durmiendo en su cama (dura 1D6 minutos).",
    "Un azafato vestido a la moda de 1923 sirve bebidas con total naturalidad en el coche salón E y desaparece al girar la esquina.",
    "El conde Fenalik aparece al final del pasillo y se lanza contra el investigador más cercano durante 1D6 minutos (usa su ficha de 1923).",
    "Una pieza original del Simulacro de Sedefkar aparece sobre una mesa o litera; se puede tocar y mover antes de desvanecerse.",
    "Unos camisas negras italianos sin rostro suben al tren y exigen con gestos mudos los pasaportes y documentos de viaje.",
    "El espantoso Príncipe Rompecabezas aparece en su trono de gemas incrustadas preguntando si hay trato (1D6 minutos).",
    "Un rostro pálido de ojos lechosos en blanco se pega al exterior de la ventanilla entre la niebla gris y mira fijamente a los viajeros (1/1D4 COR).",
    "Al abrir el grifo del lavabo brota sangre que se estanca en la pila; o bien flota un globo ocular dentro de una copa en el coche salón (1/1D4 COR).",
    "Se oye sollozar a una niña pequeña de espaldas al final del vagón; cuando alguien le pone la mano en el hombro se gira sin rostro (1/1D4 COR).",
    "El tren tiembla y se metamorfosea momentáneamente en la bestia locomotora (o un eco histórico: bandidos turcos de 1891, la ventisca de 1929 o Paul Deschanel en pijama).",
]
