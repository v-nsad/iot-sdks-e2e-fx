/*
 * Azure IOT End-to-End Test Wrapper Rest Api
 *
 * REST API definition for End-to-end testing of the Azure IoT SDKs.  All SDK APIs that are tested by our E2E tests need to be defined in this file.  This file takes some liberties with the API definitions.  In particular, response schemas are undefined, and error responses are also undefined.
 *
 * OpenAPI spec version: 1.0.0
 *
 * Generated by: https://github.com/swagger-api/swagger-codegen.git
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Primitives;
using Swashbuckle.AspNetCore.SwaggerGen;
using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using IO.Swagger.Attributes;
using IO.Swagger.Models;

namespace IO.Swagger.Controllers
{
    /// <summary>
    ///
    /// </summary>
    public class RegistryApiController : Controller
    {
        // Added 1 line in merge
        static internal RegistryGlue registry_glue = new RegistryGlue();

        /// <summary>
        /// Connect to registry
        /// </summary>
        /// <remarks>Connect to the Azure IoTHub registry.  More specifically, the SDK saves the connection string that is passed in for future use.</remarks>
        /// <param name="connectionString">connection string</param>
        /// <response code="200">OK</response>
        [HttpPut]
        [Route("/registry/connect")]
        [ValidateModelState]
        [SwaggerOperation("RegistryConnect")]
        [SwaggerResponse(statusCode: 200, type: typeof(ConnectResponse), description: "OK")]
        public virtual IActionResult RegistryConnect([FromQuery][Required()]string connectionString)
        {
            // Replaced impl in merge
            Task<ConnectResponse> t = registry_glue.ConnectAsync(connectionString);
            t.Wait();
            return new ObjectResult(t.Result);
        }

        /// <summary>
        /// Disconnect from the registry
        /// </summary>
        /// <remarks>Disconnects from the Azure IoTHub registry.  More specifically, closes all connections and cleans up all resources for the active connection</remarks>
        /// <param name="connectionId">Id for the connection</param>
        /// <response code="200">OK</response>
        [HttpPut]
        [Route("/registry/{connectionId}/disconnect/")]
        [ValidateModelState]
        [SwaggerOperation("RegistryDisconnect")]
        public virtual IActionResult RegistryDisconnect([FromRoute][Required]string connectionId)
        {
            // Replaced impl in merge
            registry_glue.DisconnectAsync(connectionId).Wait();
            return StatusCode(200);
        }

        /// <summary>
        /// gets the device twin for the given deviceid
        /// </summary>

        /// <param name="connectionId">Id for the connection</param>
        /// <param name="deviceId"></param>
        /// <response code="200">OK</response>
        [HttpGet]
        [Route("/registry/{connectionId}/deviceTwin/{deviceId}")]
        [ValidateModelState]
        [SwaggerOperation("RegistryGetDeviceTwin")]
        [SwaggerResponse(statusCode: 200, type: typeof(Twin), description: "OK")]
        public virtual IActionResult RegistryGetDeviceTwin([FromRoute][Required]string connectionId, [FromRoute][Required]string deviceId)
        {
            //TODO: Uncomment the next line to return response 200 or use other options such as return this.NotFound(), return this.BadRequest(..), ...
            // return StatusCode(200, default(Twin));

            string exampleJson = null;
            exampleJson = "{\n  \"desired\" : \"{}\",\n  \"reported\" : \"{}\"\n}";

            var example = exampleJson != null
            ? JsonConvert.DeserializeObject<Twin>(exampleJson)
            : default(Twin);
            //TODO: Change the data returned
            return new ObjectResult(example);
        }

        /// <summary>
        /// gets the module twin for the given deviceid and moduleid
        /// </summary>

        /// <param name="connectionId">Id for the connection</param>
        /// <param name="deviceId"></param>
        /// <param name="moduleId"></param>
        /// <response code="200">OK</response>
        [HttpGet]
        [Route("/registry/{connectionId}/moduleTwin/{deviceId}/{moduleId}")]
        [ValidateModelState]
        [SwaggerOperation("RegistryGetModuleTwin")]
        [SwaggerResponse(statusCode: 200, type: typeof(Twin), description: "OK")]
        public virtual IActionResult RegistryGetModuleTwin([FromRoute][Required]string connectionId, [FromRoute][Required]string deviceId, [FromRoute][Required]string moduleId)
        {
            // replaced impl in merge
            Task<Models.Twin> t = registry_glue.GetModuleTwin(connectionId, deviceId, moduleId);
            t.Wait();
            return new ObjectResult(t.Result);
        }

        /// <summary>
        /// update the device twin for the given deviceId
        /// </summary>

        /// <param name="connectionId">Id for the connection</param>
        /// <param name="deviceId"></param>
        /// <param name="twin"></param>
        /// <response code="200">OK</response>
        [HttpPatch]
        [Route("/registry/{connectionId}/deviceTwin/{deviceId}")]
        [ValidateModelState]
        [SwaggerOperation("RegistryPatchDeviceTwin")]
        public virtual IActionResult RegistryPatchDeviceTwin([FromRoute][Required]string connectionId, [FromRoute][Required]string deviceId, [FromBody]Twin twin)
        {
            //TODO: Uncomment the next line to return response 200 or use other options such as return this.NotFound(), return this.BadRequest(..), ...
            // return StatusCode(200);


            throw new NotImplementedException();
        }

        /// <summary>
        /// update the module twin for the given deviceId and moduleId
        /// </summary>

        /// <param name="connectionId">Id for the connection</param>
        /// <param name="deviceId"></param>
        /// <param name="moduleId"></param>
        /// <param name="twin"></param>
        /// <response code="200">OK</response>
        [HttpPatch]
        [Route("/registry/{connectionId}/moduleTwin/{deviceId}/{moduleId}")]
        [ValidateModelState]
        [SwaggerOperation("RegistryPatchModuleTwin")]
        public virtual IActionResult RegistryPatchModuleTwin([FromRoute][Required]string connectionId, [FromRoute][Required]string deviceId, [FromRoute][Required]string moduleId, [FromBody]Twin twin)
        {
            // replaced impl in merge
            registry_glue.PatchModuleTwin(connectionId, deviceId, moduleId, twin).Wait();
            return StatusCode(200);
        }
    }
}
