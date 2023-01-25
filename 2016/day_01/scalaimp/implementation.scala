import scala.util.control.Breaks._


@main def main(path: String) = {
    println(part_1(path))
    println(part_2(path))
}

val readInputs = (path: String) => {
    val src = io.Source.fromFile(path)
    val txt = try src.mkString finally src.close()
    txt.split(",").map(_.trim).map((x) => (x.take(1), x.drop(1).toInt))
}

val to_grid = (n : Int, angle : Int) => {
    angle match
      case 0 => (0, n)
      case 90 => (n, 0)
      case 180 => (0, -n)
      case 270 => (-n, 0)
      case _ => throw new IllegalArgumentException
}

val part_1 = (path : String) => {
    var x = 0
    var y = 0
    var angle = 0
    for ((turn, dist) <- readInputs(path)) {
        {turn match
            case "R" => angle += 90
            case "L" => angle -= 90
            case _  => throw new IllegalArgumentException
        }
        angle = (angle + 360) % 360
        val (dx, dy) = to_grid(dist, angle)
        x += dx
        y += dy
    }
    x.abs + y.abs
}

val sign = (x : Int) => if (x > 0) 1 else if (x < 0) -1 else 0

val part_2 = (path : String) => {
    var x = 0
    var y = 0
    var visited = Set((x, y))
    var angle = 0
    breakable {
        for ((turn, dist) <- readInputs(path)) {
            {turn match
                case "R" => angle += 90
                case "L" => angle -= 90
                case _  => throw new IllegalArgumentException
            }
            angle = (angle + 360) % 360     
            val (dx, dy) = to_grid(dist, angle)
            for (i <- 0 until dx.abs.max(dy.abs)) {
                x += sign(dx)
                y += sign(dy)
                if visited contains (x, y) then break
                visited += (x, y)
            }
        }
    }
    x.abs + y.abs

}