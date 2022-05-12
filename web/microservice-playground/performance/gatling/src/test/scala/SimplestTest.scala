import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class SimplestTest extends Simulation {

  val usersCount = Integer.getInteger("users", 1)
  val rampingTime  = java.lang.Long.getLong("ramp", 0L) // in seconds

  val requestJson = """{ "pmalpighiaceous": "pnonexternality", "OVERCENSURIOUS": "pantomimicry", "artigas": "bijouterie", "AFRIKAANS": "overwearying", "argones": "knickered", "CENTRODOSAL": "contentness", "untremulant": "unintrenchable", "VIPERISHLY": "remasticated", "clear": "piece", "BURRIED": "gritty", "awesome": "stiff", "RUM": "soul", "rct": "polis", "AFGHANISTAN": "yodelled", "PRELUDIOUSLY": "exemplarity", "schrik": "ekaterinburg", "albania": "gynephobia", "SHORTCUT": "subtiliser", "super": "gaillardia", "INEPTLY": "hoper", "ANDORRA": "hodgepodge" }"""

  val httpConf = http.baseURL("http://localhost:9090")

//  val scn = scenario("BasicSimulation")
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)
//    .exec(http("request_1").get("/"))
//    .pause(1)

  val scn = scenario("BasicSimulation")
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)
    .exec(http("request_1").post("/")
      .body(StringBody(requestJson)).asJSON
      .header("Content-Type", "application/json"))
    .pause(1)

  setUp(
    //scn.inject(atOnceUsers(30)
    scn.inject(rampUsers(usersCount) over rampingTime
    ).protocols(httpConf))
}
