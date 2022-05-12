/*
 * Copyright 2012-2013 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package butla.springapp;

import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
public class SampleController {

	@RequestMapping(value = "/", method = RequestMethod.GET)
	@ResponseBody
	public String helloWorld() {
		return "Hello World\n";
	}

	@RequestMapping(value = "/", method = RequestMethod.POST)
	@ResponseBody
	public HashMap<String, String> forBenchmark(@RequestBody HashMap<String, String> request) {
		HashMap<String, String> filtered = new HashMap<String, String>();
		for(Map.Entry<String, String> entry : request.entrySet())
		{
			if(entry.getKey().toLowerCase().startsWith("a"))
			{
				filtered.put(entry.getKey(), entry.getValue());
			}
		}
		return filtered;
	}

	@RequestMapping("/foo")
	@ResponseBody
	public String foo() {
		throw new IllegalArgumentException("Server error");
	}
}
