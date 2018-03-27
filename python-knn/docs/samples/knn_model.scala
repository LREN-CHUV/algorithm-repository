
// Proving that a PrettyPFA document is typesafe using a transcription to Scala

import com.opendatagroup.hadrian.data.PFAArray
import com.opendatagroup.hadrian.lib.metric.SimpleEuclidean
import com.opendatagroup.hadrian.lib.model.neighbor.NearestK

object adapters {
  type Array[A] = PFAArray[A]

  object Array {
    def apply(x: Double, xs: Double*): Array[Double] =
      PFAArray.fromVector(scala.Array.apply(x, xs).toVector.asInstanceOf[Vector[Double]])

    def apply[A](x: A, xs: A*) = ???

    def empty[A]: Array[A] = PFAArray.empty()
  }

}

import adapters._

package model {

  object neighbor {

    def nearestK[A, B](k: Int, datum: A, codebook: Array[B], metric: (A, B) => Double): Array[B] =
      new NearestK(None).apply(k, datum, codebook, metric)

  }
}

object metric {
  def simpleEuclidean(x: Array[Double], y: Array[Double]): Double =
    new SimpleEuclidean(None).apply(x, y)
}

object a {

  def map[A, B](a: Array[A], fcn: A => B): Array[B] = ???

  def mean(a: Array[Double]): Double = ???

  def flatten[A](a: Array[Array[A]]): Array[A] = ???
}


object knn_model {

  case class Query(sql: String,
    variable: String,
    covariables: Array[String])

  case class Point(
    x: Array[Double],
    y: Double)

  type Codebook = Array[Point]

  case class Input(
    subjectageyears: Int,
    rightsogsuperioroccipitalgyrus: Double
  )

  object cells {
    val codebook: Codebook = Array.empty
    val nNeighbors: Int = 5
  }

  object fcns {
    val arr: Double => Array[Double] = (x: Double) =>
      Array(x)

    val C: (String, Array[String]) => Array[Double] = (x: String, categories: Array[String]) => {
      val fcn: String => Double = (cat: String) =>
        if (cat == x)
          1 else 0

      a.map(categories, fcn)
    }

    val standardize: (Double, Double, Double) => Double = (x: Double, mu: Double, sigma: Double) =>
      (x - mu) / sigma
  }

  val u = fcns
  import cells._

  def action(input: Input): Double = {
    val x: Array[Double] = a.flatten(Array[Array[Double]](
      u.arr((input.subjectageyears.toDouble - 0.0) / 1.0),
      u.arr((input.rightsogsuperioroccipitalgyrus.toDouble - 0.0) / 1.0)
    ))

    val fcn: (Array[Double], Point) => Double = (x: Array[Double], p: Point) => {
      metric.simpleEuclidean(x, p.x)
    }

    val neighbors = model.neighbor.nearestK(nNeighbors, x, codebook, fcn)

    val fcn2: Point => Double = (p: Point) => p.y

    a.mean(a.map(neighbors, fcn2))
  }

}
